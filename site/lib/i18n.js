/* 다국어 골격.
 *
 * 언어는 세 층으로 나뉩니다. 셋의 가용 범위가 서로 다르기 때문에 따로 다룹니다.
 *
 *   1) UI 문구      i18n/ui.<lang>.json      — 4개 언어 전부 준비됨
 *   2) 학습 콘텐츠   content/<lang>/*.json    — 지금은 ko 만. 없으면 ko 로 폴백
 *   3) 시뮬레이션    ?locale=<lang>           — 시뮬레이션마다 번역 유무가 다름
 *                                              (content/sim-locales.json 에 표가 있음)
 *
 * 실제 빌드에서는 1) 2) 가 언어별 정적 HTML 로 구워지고, 3) 만 런타임 판단으로 남습니다.
 */

export const LANGS = [
  { code: 'ko', label: '한국어',   htmlLang: 'ko' },
  { code: 'en', label: 'English',  htmlLang: 'en' },
  { code: 'ja', label: '日本語',    htmlLang: 'ja' },
  { code: 'es', label: 'Español',  htmlLang: 'es' }
];

/** 기준 언어. 콘텐츠가 없을 때 여기로 떨어집니다. */
export const BASE = 'ko';

const KEY = 'nudge.lang';

export function currentLang() {
  const q = new URLSearchParams( location.search ).get( 'lang' );
  const saved = localStorage.getItem( KEY );
  const nav = ( navigator.language || '' ).slice( 0, 2 );
  for ( const c of [ q, saved, nav ] ) {
    if ( LANGS.some( l => l.code === c ) ) { return c; }
  }
  return BASE;
}

export function setLang( code ) {
  localStorage.setItem( KEY, code );
  const u = new URL( location.href );
  u.searchParams.set( 'lang', code );
  location.href = u;
}

const cache = new Map();
async function json( path ) {
  if ( !cache.has( path ) ) {
    cache.set( path, fetch( path ).then( r => ( r.ok ? r.json() : null ) ).catch( () => null ) );
  }
  return cache.get( path );
}

/** UI 문구. 키가 없으면 기준 언어로, 그것도 없으면 키 자체를 돌려줍니다. */
export async function loadUI( lang ) {
  const [ bag, base ] = await Promise.all( [
    json( `/i18n/ui.${ lang }.json` ),
    lang === BASE ? Promise.resolve( null ) : json( `/i18n/ui.${ BASE }.json` )
  ] );
  return ( key, vars ) => {
    let s = bag?.[ key ] ?? base?.[ key ];
    if ( s === undefined ) {
      console.warn( `[i18n] 빠진 키: ${ key } (${ lang })` );
      return key;
    }
    if ( vars ) {
      for ( const [ k, v ] of Object.entries( vars ) ) { s = s.replaceAll( `{${ k }}`, v ); }
    }
    return s;
  };
}

/**
 * 학습 콘텐츠. 요청한 언어에 없으면 기준 언어로 떨어지고,
 * 무엇이 실제로 쓰였는지를 함께 돌려줍니다 — 화면에 "한국어로 보여 드립니다"를 띄우기 위해서.
 */
export async function loadContent( name, lang ) {
  const want = await json( `/content/${ lang }/${ name }.json` );
  if ( want ) { return { data: want, langUsed: lang, fellBack: false }; }
  const base = await json( `/content/${ BASE }/${ name }.json` );
  return { data: base, langUsed: BASE, fellBack: lang !== BASE };
}

/** 시뮬레이션별 번역 유무 표 (언어 중립) */
export async function simLocales() {
  return ( await json( '/content/sim-locales.json' ) ) || {};
}

/** 이 시뮬레이션을 이 언어로 열 수 있는가. 없으면 영어로 엽니다. */
export function simLocaleFor( table, repo, lang ) {
  const have = table[ repo ] || [ 'en' ];
  return have.includes( lang ) ? lang : 'en';
}

export function applyDocLang( lang ) {
  const m = LANGS.find( l => l.code === lang );
  document.documentElement.lang = m ? m.htmlLang : BASE;
}

/** 상단 바에 넣는 언어 선택기 */
export function langPicker( lang ) {
  const sel = document.createElement( 'select' );
  sel.className = 'langsel';
  sel.setAttribute( 'aria-label', 'language' );
  LANGS.forEach( l => {
    const o = document.createElement( 'option' );
    o.value = l.code; o.textContent = l.label; o.selected = l.code === lang;
    sel.appendChild( o );
  } );
  sel.onchange = () => setLang( sel.value );
  return sel;
}

/** 링크에 현재 언어를 물려 줍니다 (시안이라 쿼리로, 실제 빌드에서는 /ko/ 경로로) */
export function withLang( href, lang ) {
  if ( lang === BASE ) { return href; }
  return href + ( href.includes( '?' ) ? '&' : '?' ) + 'lang=' + lang;
}
