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

console.log( `\n오류 ${ errors } · 경고 ${ warns }\n` );
process.exit( errors ? 1 : 0 );
