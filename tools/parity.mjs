/* 언어 대조 검사 — 번역본이 한국어 원고와 같은 뼈대인지 봅니다.
 *
 *   node tools/parity.mjs
 *
 * lint.mjs 는 태그와 조판만 봅니다. 번역본의 구조가 ko 와 같은지는 아무도
 * 보지 않아서, 선택지 순서가 바뀌어 right 가 어긋나거나 번역 금지 필드가
 * 옮겨지는 사고를 잡을 곳이 없었습니다. 세 언어 × 29만 자를 눈으로 지킬 수는
 * 없으므로 이 파일이 그 자리를 맡습니다. docs/I18N-BRIEF.md §8 의 함정 2·3 입니다.
 *
 * site/content/<lang>/ 은 완성본이라 키가 하나라도 빠지면 오류입니다.
 * wip/<lang>/ 은 작업 중이라 빠진 항목을 진행률로만 알립니다.
 */
import fs from 'node:fs';

const BASE = 'ko';
const LANGS = [ 'en', 'ja', 'es' ];
const FILES = [ 'courses', 'lessons', 'guides' ];

/* 코드가 읽는 값. 번역하면 화면이 깨지거나 채점이 틀립니다. */
const FROZEN = [ 'id', 'no', 'course', 'sim', 'mode' ];
/* 이 길이 이상인데 한국어와 글자가 똑같으면 옮기다 만 자리로 봅니다. */
const SUSPECT = 12;

let errors = 0, warns = 0;
/* 통째로 복사해 둔 파일이면 '글자가 같음' 이 수천 줄 나옵니다.
   파일마다 앞 열 줄만 보이고 나머지는 개수로 접습니다. */
const SHOW_SAME = 10;
let same = 0;
const err = m => { console.log( '  ✗ ' + m ); errors++; };
const warn = m => { console.log( '  ! ' + m ); warns++; };
const ok = m => console.log( '  ✓ ' + m );

const read = p => {
  try { return JSON.parse( fs.readFileSync( p, 'utf8' ) ); }
  catch { return null; }
};

const type = v => Array.isArray( v ) ? 'array' : ( v === null ? 'null' : typeof v );

/* base 와 tgt 를 나란히 걷습니다. frozen 은 'sims' 처럼 배열째 번역 금지인
   자리에서 아래로 물려 줍니다. */
const walk = ( base, tgt, path, key, frozen ) => {
  const tb = type( base ), tt = type( tgt );
  if ( tb !== tt ) { err( `${ path }: ko 는 ${ tb } 인데 ${ tt }` ); return; }

  if ( tb === 'array' ) {
    if ( base.length !== tgt.length ) {
      err( `${ path }: 개수가 다름 — ko ${ base.length } vs ${ tgt.length }` );
      return;
    }
    const f = frozen || key === 'sims';
    base.forEach( ( v, i ) => walk( v, tgt[ i ], `${ path }[${ i }]`, key, f ) );
    return;
  }

  if ( tb === 'object' ) {
    const bk = Object.keys( base ), tk = Object.keys( tgt );
    for ( const k of bk ) {
      if ( !( k in tgt ) ) { err( `${ path }/${ k }: 빠짐` ); }
    }
    for ( const k of tk ) {
      if ( !( k in base ) ) { err( `${ path }/${ k }: ko 에 없는 키` ); }
    }
    for ( const k of bk ) {
      if ( k in tgt ) { walk( base[ k ], tgt[ k ], `${ path }/${ k }`, k, frozen ); }
    }
    return;
  }

  if ( tb === 'string' ) {
    if ( frozen || FROZEN.includes( key ) ) {
      if ( base !== tgt ) { err( `${ path }: 번역 금지 값이 바뀜 — "${ base }" → "${ tgt }"` ); }
    }
    else if ( base === tgt && base.length >= SUSPECT ) {
      same++;
      if ( same <= SHOW_SAME ) { warn( `${ path }: 한국어와 글자가 같음 — 옮기다 만 자리?` ); }
      else { warns++; }
    }
    return;
  }

  /* 숫자 · 참거짓 — screens · min · diff · minutes · ready · right 가 여기 옵니다.
     right 가 어긋나면 오답이 정답이 됩니다. */
  if ( base !== tgt ) { err( `${ path }: 번역 금지 값이 바뀜 — ${ base } → ${ tgt }` ); }
};

/* right 는 0 부터 세는 인덱스입니다. 범위를 벗어나면 채점이 조용히 실패합니다. */
const checkRight = ( node, path, label ) => {
  if ( Array.isArray( node ) ) {
    node.forEach( ( v, i ) => checkRight( v, `${ path }[${ i }]`, label ) );
    return;
  }
  if ( !node || typeof node !== 'object' ) { return; }
  if ( typeof node.right === 'number' ) {
    const opts = Array.isArray( node.opts ) ? node.opts : null;
    if ( opts && ( node.right < 0 || node.right >= opts.length ) ) {
      err( `${ label } ${ path }/right: ${ node.right } — 선택지 ${ opts.length }개 범위 밖` );
    }
  }
  for ( const [ k, v ] of Object.entries( node ) ) {
    if ( v && typeof v === 'object' ) { checkRight( v, `${ path }/${ k }`, label ); }
  }
};

/* ── 검사 ────────────────────────────────────────────────── */

console.log( '\n[P0] right 인덱스 범위 (한국어 포함 전부)' );
{
  const before = errors;
  for ( const L of [ BASE, ...LANGS ] ) {
    for ( const dir of [ `site/content/${ L }`, `wip/${ L }` ] ) {
      const l = read( `${ dir }/lessons.json` );
      if ( l ) { checkRight( l, '', `${ dir }/lessons.json` ); }
    }
  }
  if ( errors === before ) { ok( '모든 right 가 선택지 개수 안에 있음' ); }
}

for ( const name of FILES ) {
  console.log( `\n[P] ${ name }.json — 한국어와 뼈대 대조` );
  const base = read( `site/content/${ BASE }/${ name }.json` );
  if ( !base ) { err( `site/content/${ BASE }/${ name }.json 을 읽을 수 없음` ); continue; }
  const baseTop = Object.keys( base ).filter( k => k !== '_note' );

  let seen = 0;
  for ( const L of LANGS ) {
    for ( const [ dir, partial ] of [ [ `site/content/${ L }`, false ], [ `wip/${ L }`, true ] ] ) {
      const tgt = read( `${ dir }/${ name }.json` );
      if ( !tgt ) { continue; }
      seen++;
      const before = { e: errors, w: warns };

      /* 작업 중인 파일은 아직 없는 항목을 진행률로만 봅니다. */
      const have = baseTop.filter( k => k in tgt );
      const missing = baseTop.filter( k => !( k in tgt ) );
      if ( partial && missing.length ) {
        console.log( `  … ${ dir }/${ name }.json — ${ have.length }/${ baseTop.length } 작업 중` );
      }
      else if ( missing.length ) {
        missing.forEach( k => err( `${ dir }/${ name }.json /${ k }: 빠짐` ) );
      }
      /* 밑줄로 시작하는 맨 위 키는 사람이 읽는 메모입니다. 그 언어에만 있어도 됩니다. */
      for ( const k of Object.keys( tgt ) ) {
        if ( !baseTop.includes( k ) && !k.startsWith( '_' ) ) {
          err( `${ dir }/${ name }.json /${ k }: ko 에 없는 키` );
        }
      }
      for ( const k of have ) {
        walk( base[ k ], tgt[ k ], `${ dir }/${ name }.json /${ k }`, k, false );
      }

      if ( same > SHOW_SAME ) {
        console.log( `  ! … 한국어와 글자가 같은 자리 ${ same }곳 (앞 ${ SHOW_SAME }곳만 보임)` );
      }
      same = 0;
      if ( errors === before.e && warns === before.w ) {
        ok( `${ dir }/${ name }.json — 뼈대 일치${ partial && missing.length ? ' (작업 중인 부분까지)' : '' }` );
      }
    }
  }
  if ( !seen ) { console.log( '  … 대조할 번역본이 아직 없음' ); }
}

console.log( `\n오류 ${ errors } · 경고 ${ warns }\n` );
process.exit( errors ? 1 : 0 );
