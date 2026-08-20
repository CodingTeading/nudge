/* 검색·공유용 머리말.
 *
 * ⚠ 시안이라 자바스크립트로 채워 넣습니다. 실제 빌드에서는 반드시 **정적 HTML 로 구워야**
 *   합니다. 구글은 JS 를 실행해 주지만 **카카오톡·네이버·페이스북의 미리보기 수집기는
 *   실행하지 않습니다.** 한국 학생들이 링크를 나르는 곳이 카카오톡이라, 여기가 비면
 *   공유 카드가 통째로 빈 채로 돌아다니게 됩니다.
 *   그래서 각 HTML 의 <head> 에 한국어 기준값을 이미 박아 두었고, 이 모듈은
 *   언어가 바뀌었을 때 그 값을 갱신하는 역할만 합니다.
 */

import { LANGS, BASE } from './i18n.js';

/* 배포 주소. 실제 도메인이 정해지면 여기 한 곳만 고칩니다. */
export const ORIGIN = 'https://nudge.codingteading.com';

const OG_LOCALE = { ko: 'ko_KR', en: 'en_US', ja: 'ja_JP', es: 'es_ES' };

function meta( attr, key, content ) {
  if ( !content ) { return; }
  let el = document.head.querySelector( `meta[${ attr }="${ key }"]` );
  if ( !el ) {
    el = document.createElement( 'meta' );
    el.setAttribute( attr, key );
    document.head.appendChild( el );
  }
  el.setAttribute( 'content', content );
}

function link( rel, href, extra ) {
  const el = document.createElement( 'link' );
  el.rel = rel;
  el.href = href;
  if ( extra ) { Object.entries( extra ).forEach( ( [ k, v ] ) => el.setAttribute( k, v ) ); }
  document.head.appendChild( el );
}

/** 검색 결과에서 잘리지 않게 자릅니다. 한국어는 글자당 폭이 커서 기준이 다릅니다. */
function clamp( s, lang ) {
  const max = ( lang === 'ko' || lang === 'ja' ) ? 90 : 158;
  s = String( s || '' ).replace( /\s+/g, ' ' ).trim();
  return s.length <= max ? s : s.slice( 0, max - 1 ).replace( /[\s,·]+$/, '' ) + '…';
}

/**
 * @param {object} o
 *   lang, title, desc, path   — path 는 언어 없는 경로 ('lesson.html?l=static-2')
 *   image                     — og/*.png 의 파일명
 *   jsonld                    — 구조화 데이터 객체(또는 배열)
 */
export function applySeo( o ) {
  const { lang, title, desc, path, image, keywords, jsonld } = o;
  const d = clamp( desc, lang );

  document.title = title;
  meta( 'name', 'description', d );
  if ( keywords ) { meta( 'name', 'keywords', keywords ); }

  const url = ORIGIN + '/' + ( lang === BASE ? path : path + ( path.includes( '?' ) ? '&' : '?' ) + 'lang=' + lang );
  const img = ORIGIN + '/og/' + ( image || 'default.png' );

  link( 'canonical', url );

  /* hreflang — 같은 문서의 다른 언어판을 서로 알려 줍니다.
     이게 없으면 네 언어판이 서로 중복 문서로 취급될 수 있습니다. */
  LANGS.forEach( l => {
    const href = ORIGIN + '/' + ( l.code === BASE ? path
      : path + ( path.includes( '?' ) ? '&' : '?' ) + 'lang=' + l.code );
    link( 'alternate', href, { hreflang: l.htmlLang } );
  } );
  link( 'alternate', ORIGIN + '/' + path, { hreflang: 'x-default' } );

  meta( 'property', 'og:type', 'website' );
  meta( 'property', 'og:site_name', 'Nudge' );
  meta( 'property', 'og:title', title );
  meta( 'property', 'og:description', d );
  meta( 'property', 'og:url', url );
  meta( 'property', 'og:image', img );
  meta( 'property', 'og:image:width', '1200' );
  meta( 'property', 'og:image:height', '630' );
  meta( 'property', 'og:image:alt', title );
  meta( 'property', 'og:locale', OG_LOCALE[ lang ] || 'ko_KR' );
  LANGS.filter( l => l.code !== lang )
    .forEach( l => meta( 'property', 'og:locale:alternate', OG_LOCALE[ l.code ] ) );

  meta( 'name', 'twitter:card', 'summary_large_image' );
  meta( 'name', 'twitter:title', title );
  meta( 'name', 'twitter:description', d );
  meta( 'name', 'twitter:image', img );

  if ( jsonld ) {
    const s = document.createElement( 'script' );
    s.type = 'application/ld+json';
    s.textContent = JSON.stringify( jsonld );
    document.head.appendChild( s );
  }
}

/** 사이트 공통 구조화 데이터 — 홈에만 붙입니다. */
export function siteJsonLd( t ) {
  return [ {
    '@context': 'https://schema.org',
    '@type': 'EducationalOrganization',
    name: 'Nudge',
    url: ORIGIN,
    logo: ORIGIN + '/brand/mark.svg',
    description: t( 'seo.home.desc' ),
    isAccessibleForFree: true
  }, {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'Nudge',
    url: ORIGIN,
    inLanguage: LANGS.map( l => l.htmlLang ),
    potentialAction: {
      '@type': 'SearchAction',
      target: { '@type': 'EntryPoint', urlTemplate: ORIGIN + '/all.html?q={search_term_string}' },
      'query-input': 'required name=search_term_string'
    }
  } ];
}

/** 코스 한 개 = schema.org 의 Course */
export function courseJsonLd( c, lessons, lang ) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Course',
    name: c.title,
    description: c.lead,
    url: ORIGIN + '/course.html?c=' + c.id,
    inLanguage: lang,
    isAccessibleForFree: true,
    educationalLevel: 'secondary education',
    about: c.subject,
    timeRequired: 'PT' + c.minutes + 'M',
    provider: { '@type': 'EducationalOrganization', name: 'Nudge', url: ORIGIN },
    hasCourseInstance: {
      '@type': 'CourseInstance',
      courseMode: 'online',
      courseWorkload: 'PT' + c.minutes + 'M'
    },
    syllabusSections: lessons.map( ( l, i ) => ( {
      '@type': 'Syllabus',
      name: l.title,
      position: i + 1,
      timeRequired: 'PT' + l.min + 'M'
    } ) )
  };
}

/** 레슨 한 편 = LearningResource + 빵부스러기 */
export function lessonJsonLd( L, meta_, course, lang ) {
  return [ {
    '@context': 'https://schema.org',
    '@type': 'LearningResource',
    name: L.title,
    description: L.lead,
    url: ORIGIN + '/lesson.html?l=' + meta_.id,
    inLanguage: lang,
    isAccessibleForFree: true,
    learningResourceType: 'interactive simulation lesson',
    educationalLevel: 'secondary education',
    timeRequired: 'PT' + meta_.min + 'M',
    teaches: course.title,
    isPartOf: { '@type': 'Course', name: course.title, url: ORIGIN + '/course.html?c=' + course.id }
  }, {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Nudge', item: ORIGIN + '/' },
      { '@type': 'ListItem', position: 2, name: course.title, item: ORIGIN + '/course.html?c=' + course.id },
      { '@type': 'ListItem', position: 3, name: L.title }
    ]
  } ];
}
