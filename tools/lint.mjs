/* 시안 정합성 검사.
 *
 * aiTeadingForTeens 의 `npm run lint` 가 하는 일을 축소해서 옮겨 온 것입니다.
 * 실제 빌드로 옮길 때 build/lint.mjs 의 출발점이 됩니다.
 *
 *   node .claude/proto-lint.mjs
 */
import fs from 'node:fs';

const ROOT = 'site';
/* 시뮬레이션 산출물은 PhET 포크 쪽에 있습니다 (README 참고).
   경로를 환경변수로 덮어쓸 수 있게 열어 둡니다. */
const SIMS = process.env.NUDGE_SIMS || '../phet/deploy/sims.json';
const LANGS = [ 'ko', 'en', 'ja', 'es' ];
const BASE = 'ko';

let errors = 0, warns = 0;
const err = m => { console.log( '  ✗ ' + m ); errors++; };
const warn = m => { console.log( '  ! ' + m ); warns++; };
const ok = m => console.log( '  ✓ ' + m );

const read = p => {
  try { return JSON.parse( fs.readFileSync( `${ ROOT }/${ p }`, 'utf8' ) ); }
  catch ( e ) { return null; }
};

/* ── 1. UI 문구 키 집합이 언어마다 같은가 ── */
console.log( '\n[1] UI 문구 키 일치' );
const base = read( `i18n/ui.${ BASE }.json` );
if ( !base ) { err( `i18n/ui.${ BASE }.json 을 읽을 수 없음` ); }
else {
  const baseKeys = Object.keys( base ).filter( k => !k.startsWith( '_' ) );
  for ( const L of LANGS ) {
    if ( L === BASE ) { continue; }
    const bag = read( `i18n/ui.${ L }.json` );
    if ( !bag ) { err( `ui.${ L }.json 없음` ); continue; }
    const keys = new Set( Object.keys( bag ) );
    const missing = baseKeys.filter( k => !keys.has( k ) );
    const extra = [ ...keys ].filter( k => !k.startsWith( '_' ) && !baseKeys.includes( k ) );
    if ( missing.length ) { err( `${ L }: 빠진 키 ${ missing.length }개 — ${ missing.join( ', ' ) }` ); }
    if ( extra.length ) { warn( `${ L }: 기준에 없는 키 — ${ extra.join( ', ' ) }` ); }
    if ( !missing.length && !extra.length ) { ok( `${ L } — ${ baseKeys.length }개 키 모두 일치` ); }
  }

  /* ── 2. 자리표시자 {name} 개수가 같은가 ── */
  console.log( '\n[2] 자리표시자 일치' );
  let bad = 0;
  const holes = s => ( String( s ).match( /\{[a-zA-Z]+\}/g ) || [] ).sort().join( ',' );
  for ( const L of LANGS ) {
    if ( L === BASE ) { continue; }
    const bag = read( `i18n/ui.${ L }.json` ) || {};
    for ( const k of baseKeys ) {
      if ( bag[ k ] === undefined ) { continue; }
      if ( holes( base[ k ] ) !== holes( bag[ k ] ) ) {
        err( `${ L }/${ k }: ${ BASE }=[${ holes( base[ k ] ) }] vs ${ L }=[${ holes( bag[ k ] ) }]` );
        bad++;
      }
    }
  }
  if ( !bad ) { ok( '모든 언어의 자리표시자가 기준과 같음' ); }
}

/* ── 3. 코스가 배포된 시뮬레이션을 빠짐없이, 중복 없이 덮는가 ── */
console.log( '\n[3] 코스 ↔ 시뮬레이션 대응' );
const sims = JSON.parse( fs.readFileSync( SIMS, 'utf8' ) ).map( s => s.repo );
const courses = read( `content/${ BASE }/courses.json` );
if ( !courses ) { err( 'courses.json 을 읽을 수 없음' ); }
else {
  const used = courses.courses.flatMap( c => c.sims );
  const dup = used.filter( ( s, i ) => used.indexOf( s ) !== i );
  const orphan = sims.filter( s => !used.includes( s ) );
  const ghost = used.filter( s => !sims.includes( s ) );
  if ( dup.length ) { err( `두 코스에 겹침: ${ [ ...new Set( dup ) ].join( ', ' ) }` ); }
  if ( orphan.length ) { err( `어느 코스에도 없음 (${ orphan.length }): ${ orphan.join( ', ' ) }` ); }
  if ( ghost.length ) { err( `배포에 없는 시뮬레이션 참조: ${ ghost.join( ', ' ) }` ); }
  if ( !dup.length && !orphan.length && !ghost.length ) {
    ok( `코스 ${ courses.courses.length }개가 시뮬레이션 ${ sims.length }종을 중복 없이 전부 덮음` );
  }
}

/* ── 4. ready 로 표시된 레슨은 본문이 있는가 ── */
console.log( '\n[4] 레슨 본문' );
const lessons = read( `content/${ BASE }/lessons.json` ) || {};
let ready = 0, missingBody = 0;
for ( const [ cid, list ] of Object.entries( courses?.lessons || {} ) ) {
  for ( const l of list ) {
    if ( !l.ready ) { continue; }
    ready++;
    if ( !lessons[ l.id ] ) { err( `${ cid }/${ l.id }: ready 인데 lessons.json 에 본문 없음` ); missingBody++; }
  }
}
if ( ready && !missingBody ) { ok( `본문이 준비된 레슨 ${ ready }개 모두 확인` ); }
if ( !ready ) { warn( 'ready 로 표시된 레슨이 없음' ); }

/* 본문의 정답 번호가 선택지 범위 안에 있는가 */
for ( const [ id, L ] of Object.entries( lessons ) ) {
  if ( id.startsWith( '_' ) ) { continue; }   // _note 같은 메모 키는 건너뜁니다
  if ( L.explain?.right >= L.predict?.opts?.length ) { err( `${ id }: explain.right 가 선택지 범위 밖` ); }
  L.quiz?.forEach( ( q, i ) => {
    if ( q.right >= q.opts.length ) { err( `${ id }/quiz[${ i }]: right 가 선택지 범위 밖` ); }
  } );
  if ( !sims.includes( L.sim ) ) { err( `${ id }: 배포에 없는 시뮬레이션 ${ L.sim }` ); }
}

/* ── 5. 사용법이 준비된 시뮬레이션 ── */
console.log( '\n[5] 사용 방법' );
const guides = read( `content/${ BASE }/guides.json` ) || {};
const guided = Object.keys( guides ).filter( k => !k.startsWith( '_' ) );
const badRepo = guided.filter( r => !sims.includes( r ) );
if ( badRepo.length ) { err( `배포에 없는 시뮬레이션의 사용법: ${ badRepo.join( ', ' ) }` ); }
if ( !guides._common ) { err( '_common (공통 조작) 이 없음' ); }
ok( `사용법 ${ guided.length }/${ sims.length } — 남은 ${ sims.length - guided.length }종은 작성 대기` );

/* ── 6. 시뮬레이션 언어표 ── */
console.log( '\n[6] 시뮬레이션 언어표' );
const table = read( 'content/sim-locales.json' ) || {};
const notInTable = sims.filter( s => !table[ s ] );
if ( notInTable.length ) { err( `표에 없는 시뮬레이션: ${ notInTable.join( ', ' ) }` ); }
else {
  const per = LANGS.map( L => `${ L } ${ sims.filter( s => table[ s ].includes( L ) ).length }` ).join( ' · ' );
  ok( `${ sims.length }종 모두 등재 — 번역 보유: ${ per }` );
}

/* ── 7. 본문 조판 ── */
console.log( '\n[7] 본문 조판' );
{
  /* lesson.html / course.html 이 평문으로 그리는 자리. 여기에 태그를 넣으면
     글자 그대로 보입니다. title 은 <title> 과 OG 에도 들어갑니다. */
  const PLAIN = { lessons: [ 'title' ], courses: [ 'title', 'hook', 'lead' ] };

  /* 한국어 조사는 앞말에 붙습니다. 굵은 글씨 뒤에 띄고 조사가 오면 어색합니다.
     앞이 문장 끝이면 뒤의 '이/그/저'는 관형사이므로 뺍니다. */
  const JOSA = '을|를|이|가|은|는|와|과|의|로|으로|만|도|부터|까지|에서|에게|보다|입니다|이고|이라|라고';
  const LOOSE_JOSA = new RegExp( `(?<![.!?])</b>[  ]+(${ JOSA })(?![가-힣])` );
  const LABEL_COLON = /:\s*<\/b>/;

  /* 붙여넣기 사고로 들어오는 폭 없는 공백·방향 표시 문자. 눈에 안 보여 찾기 어렵습니다. */
  const ZERO_WIDTH = /[​-‏‪-‮﻿]/;

  /* 본문에 쓰기로 한 태그만 허용하고, 열고 닫힌 짝이 맞는지 셉니다. */
  const ALLOWED = [ 'b', 'strong', 'em', 'i', 'p', 'ul', 'ol', 'li', 'br', 'span', 'sup', 'sub' ];
  const checkTags = str => {
    if ( !str.includes( '<' ) ) { return null; }
    const open = {};
    const re = /<(\/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>/g;
    let m, seen = 0;
    while ( ( m = re.exec( str ) ) !== null ) {
      seen++;
      const [ , slash, name, rest ] = m;
      if ( !ALLOWED.includes( name.toLowerCase() ) ) { return `허용하지 않는 태그 <${ name }>`; }
      if ( name.toLowerCase() === 'br' ) { continue; }
      if ( slash && rest.trim() ) { return `닫는 태그에 군더더기: ${ m[ 0 ] }`; }
      open[ name ] = ( open[ name ] || 0 ) + ( slash ? -1 : 1 );
      if ( open[ name ] < 0 ) { return `짝 없이 닫힌 </${ name }>`; }
    }
    /* '<' 는 있는데 태그로 안 읽혔다면 깨진 태그입니다. */
    const angles = ( str.match( /</g ) || [] ).length;
    if ( angles !== seen ) { return '깨진 태그가 있음' ; }
    const left = Object.entries( open ).find( ( [ , n ] ) => n !== 0 );
    if ( left ) { return `닫히지 않은 <${ left[ 0 ] }>` ; }
    return null;
  };

  let typo = 0;
  const scan = ( node, path, plainFields ) => {
    if ( Array.isArray( node ) ) {
      node.forEach( ( v, i ) => scan( v, `${ path }[${ i }]`, plainFields ) );
      return;
    }
    if ( !node || typeof node !== 'object' ) { return; }
    for ( const [ k, v ] of Object.entries( node ) ) {
      const here = `${ path }/${ k }`;
      if ( typeof v === 'string' ) {
        if ( plainFields.includes( k ) && v.includes( '<' ) ) {
          err( `${ here }: 평문으로 그려지는 자리에 태그가 있음` );
        }
        if ( LOOSE_JOSA.test( v ) ) { warn( `${ here }: 굵은 글씨와 조사 사이가 떠 있음` ); typo++; }
        if ( LABEL_COLON.test( v ) ) { warn( `${ here }: 굵은 글씨가 콜론으로 끝남` ); typo++; }
        if ( ZERO_WIDTH.test( v ) ) { err( `${ here }: 보이지 않는 문자가 섞여 있음` ); }
        const tagErr = checkTags( v );
        if ( tagErr ) { err( `${ here }: ${ tagErr }` ); }
      }
      else { scan( v, here, plainFields ); }
    }
  };

  /* 있는 언어는 전부 봅니다. 새 언어 원고가 검사 없이 들어오면
     태그 깨짐과 보이지 않는 문자를 아무도 못 잡습니다. */
  /* wip/ 도 같이 봅니다. 번역이 거기서 몇 달을 머무는데 그동안 태그 깨짐을
     아무도 못 잡으면, 옮겨 오는 날 한꺼번에 터집니다. */
  for ( const L of LANGS ) {
    for ( const [ where, dir ] of [ [ L, `content/${ L }` ], [ `${ L }·wip`, `../wip/${ L }` ] ] ) {
      const l = read( `${ dir }/lessons.json` );
      if ( l ) { scan( l, `lessons(${ where })`, PLAIN.lessons ); }
      const g = read( `${ dir }/guides.json` );
      if ( g ) { scan( g, `guides(${ where })`, [] ); }
      const c = read( `${ dir }/courses.json` );
      if ( c ) { scan( c, `courses(${ where })`, PLAIN.courses ); }
    }
  }
  if ( !typo ) { ok( '태그 · 조사 띄어쓰기 · 레이블 콜론 이상 없음' ); }
}

/* ── [8] 코스 시간 ─────────────────────────────────────────────
   courses[].minutes 는 그 코스 레슨 min 의 합입니다. 손으로 적는 값이라
   레슨을 더하거나 시간을 고칠 때 조용히 어긋납니다. */
{
  console.log( '\n[8] 코스 시간 합' );
  let bad = 0;
  for ( const L of LANGS ) {
    const c = read( `content/${ L }/courses.json` );
    if ( !c ) { continue; }
    for ( const course of c.courses ) {
      const rows = c.lessons[ course.id ] || [];
      const sum = rows.reduce( ( a, r ) => a + ( r.min || 0 ), 0 );
      if ( sum !== course.minutes ) {
        err( `courses(${ L })/${ course.id }: minutes ${ course.minutes } ≠ 레슨 합 ${ sum }` );
        bad++;
      }
    }
  }
  if ( !bad ) { ok( '코스마다 minutes 가 레슨 min 의 합과 일치' ); }
}

/* ── [9] 화면에 없는 이름 ───────────────────────────────────────
   이 사이트의 1번 규칙 — 학습자가 화면에서 못 찾을 글자를 원고가 인용하면 안 됩니다.
   PhET 은 아이콘만 있는 단추에 `a11y.*` 로 접근성 이름을 붙여 두는데, 그 이름은
   스크린리더 전용이라 어느 언어로도 그려지지 않습니다. 원고를 쓰다 보면 그걸
   화면 글자로 착각하기 쉽습니다 (의뢰서 §4-2).

   대조 기준은 `wip/labels/<lang>/<repo>.json` 의 `screen` · `common` 입니다.
   생성물이라 저장소에 없으므로, 없으면 건너뜁니다 — `python tools/labels.py`.

   **한국어·일본어 원고만 봅니다.** CJK 원고에서 로마자가 굵게 묶여 있으면 그건
   화면 글자를 인용한 것이 거의 확실합니다. 영어·스페인어 원고에서는
   `<b>Start here</b>` 같은 강조와 라벨 인용을 기계가 가를 수 없어 — 둘 다 로마자라 —
   시끄러운 검사가 되느니 안 보는 편이 낫다고 판단했습니다. 그쪽은 사람이 봐야 합니다.
   ───────────────────────────────────────────────────────────── */
console.log( '\n[9] 화면에 없는 이름' );
{
  const LAB = '../wip/labels';
  const shared = read( `${ LAB }/_shared_placeholder` );   /* 자리 채우기용 (아래에서 언어별로 읽습니다) */
  void shared;

  /* 우리 표기이지 화면 글자가 아닌 것들. 화학식·수식·단위가 대부분입니다. */
  const NOT_LABEL = /[0-9₀-₉⁰-⁹⁺⁻°=+×÷→←↔≠≈…％%]/;
  const HAS_CJK = /[가-힣ぁ-んァ-ヴ一-龥]/;

  /* 화면 이름 후보만 남깁니다. 소문자로 시작하거나 전부 대문자면 뺍니다
     (IQR · MAD 같은 약어는 실제 라벨이어도 놓치는 편이 시끄러운 것보다 낫습니다). */
  const looksLikeLabel = s =>
    s.length >= 3 && /^[A-Z]/.test( s ) && /[a-z]/.test( s ) &&
    /[A-Za-z]{3}/.test( s ) &&      /* 'F/f' 같은 우리 표기를 뺍니다 — 낱글자 나열입니다 */
    !NOT_LABEL.test( s ) && !HAS_CJK.test( s ) && /^[A-Za-z][A-Za-z ()/'’.-]*$/.test( s );

  /* 'Organize (왼쪽) — 가지런히 놓기' → 'Organize'
     'Hide Left / Right Counting Area' → 두 갈래로 나눠 각각 봅니다. */
  const pieces = raw => String( raw )
    .split( /[(（—–]/ )[ 0 ]
    .split( /[·•]/ )
    .flatMap( s => s.includes( '/' ) ? [ s, ...s.split( '/' ) ] : [ s ] )
    .map( s => s.trim().replace( /[:：]$/, '' ).replace( /^["'“”]|["'“”]$/g, '' ).trim() );

  /* 화면 문자열 다듬기 — <br> 같은 태그와 겹친 공백을 걷어 냅니다.
     'Polarizing<br>Beam<br>Splitter' 가 화면에서는 한 줄로 읽히기 때문입니다. */
  const flatten = s => String( s )
    .replace( /<[^>]*>/g, ' ' ).replace( / /g, ' ' ).replace( /\s+/g, ' ' ).trim();

  const BOLD = /<b>([^<]{2,60})<\/b>/g;
  const bolds = obj => {
    const out = [];
    let m;
    const s = JSON.stringify( obj );
    while ( ( m = BOLD.exec( s ) ) !== null ) { out.push( ...pieces( m[ 1 ] ) ); }
    return out;
  };

  /* CJK 원고에서만 로마자 인용이 곧 화면 글자 인용입니다 (위 설명 참고). */
  const CJK = [ 'ko', 'ja' ];

  let checked = 0, missing = 0, skipped = [];
  for ( const L of LANGS ) {
    if ( !CJK.includes( L ) ) { continue; }
    const guides = read( `content/${ L }/guides.json` );
    const lessons = read( `content/${ L }/lessons.json` );
    if ( !guides ) { continue; }
    /* 그 언어의 화면 글자 사전이 있어야 대조할 수 있습니다. */
    const probe = read( `${ LAB }/${ L }/_shared.json` );
    if ( !probe ) { skipped.push( L ); continue; }

    /* joist · scenery-phet · sun · vegas — 61종 전부에 딸려 오는 공통 화면 글자.
       영어로 열리는 실험은 이 공통 글자도 영어로 나오므로 사전을 갈아 끼웁니다. */
    const sharedOf = {};
    const commonSet = code => {
      if ( sharedOf[ code ] ) { return sharedOf[ code ]; }
      const bag = code === L ? probe : read( `${ LAB }/${ code }/_shared.json` );
      const out = new Set();
      for ( const sec of Object.values( bag || {} ) ) {
        for ( const v of Object.values( sec.screen || {} ) ) {
          if ( typeof v === 'string' ) { out.add( flatten( v ) ); }
        }
      }
      sharedOf[ code ] = out;
      return out;
    };

    for ( const repo of Object.keys( guides ) ) {
      if ( repo.startsWith( '_' ) ) { continue; }
      const dict = read( `${ LAB }/${ L }/${ repo }.json` );
      if ( !dict ) { continue; }

      const screen = new Set( commonSet( dict.opensIn || L ) );
      for ( const bag of [ dict.screen, dict.common ] ) {
        for ( const v of Object.values( bag || {} ) ) {
          if ( typeof v === 'string' ) { screen.add( flatten( v ) ); }
        }
      }
      /* `{{item}} to Prepare` 처럼 자리표시자가 든 글자는 화면에서 채워져 나옵니다.
         남는 조각이 전부 후보 안에 있으면 그 화면 글자를 인용한 것으로 봅니다. */
      const onScreen = t => [ ...screen ].some( s => {
        if ( s === t || s.includes( t ) ) { return true; }
        if ( !s.includes( '{{' ) ) { return false; }
        const bits = s.split( /\{\{[^}]*\}\}/ ).map( x => x.trim() ).filter( x => x.length >= 3 );
        return bits.length > 0 && bits.every( b => t.includes( b ) );
      } );

      /* 후보 모으기 — 조작 이름표와 굵은 글씨 인용 */
      const cand = new Map();
      const add = ( t, where ) => {
        if ( !looksLikeLabel( t ) ) { return; }
        if ( !cand.has( t ) ) { cand.set( t, where ); }
      };
      ( guides[ repo ].controls || [] ).forEach( ( c, i ) => {
        pieces( c.name ).forEach( t => add( t, `guides(${ L })/${ repo }/controls[${ i }].name` ) );
      } );
      bolds( guides[ repo ] ).forEach( t => add( t, `guides(${ L })/${ repo }` ) );
      for ( const [ lid, les ] of Object.entries( lessons || {} ) ) {
        if ( lid.startsWith( '_' ) || les.sim !== repo ) { continue; }
        bolds( les ).forEach( t => add( t, `lessons(${ L })/${ lid }` ) );
      }

      for ( const [ t, where ] of cand ) {
        checked++;
        if ( onScreen( t ) ) { continue; }
        const inA11y = ( dict.hidden || [] ).some(
          h => String( h ).toLowerCase().replace( /[._]/g, '' )
            .includes( t.toLowerCase().replace( /[ /]/g, '' ) ) );
        err( `${ where }: "${ t }" — 화면에 없음${ inA11y ? ' (a11y 전용)' : '' }` );
        missing++;
      }
    }
  }

  if ( skipped.length ) {
    console.log( `  … ${ skipped.join( ' · ' ) } 는 화면 글자 사전이 없어 건너뜀 — python tools/labels.py` );
  }
  if ( !missing && checked ) { ok( `인용한 이름 ${ checked }개가 모두 화면에 있음` ); }
  else if ( !checked ) { console.log( '  … 대조할 사전이 없어 검사하지 못함' ); }
}

console.log( `\n오류 ${ errors } · 경고 ${ warns }\n` );
process.exit( errors ? 1 : 0 );
