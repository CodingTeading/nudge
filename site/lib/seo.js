/* 검색·공유용 머리말.
 *
 * 머리말은 tools/bake-head.py 가 코스·레슨마다 **정적 HTML 로 구워 둡니다.**
 * 구글은 자바스크립트를 실행해 주지만 카카오톡·네이버·페이스북의 미리보기 수집기는
 * 실행하지 않기 때문입니다. 한국 학생들이 링크를 나르는 곳이 카카오톡이라,
 * 여기가 비면 공유 카드가 통째로 빈 채 돌아다니게 됩니다.
 *
 * 이 모듈은 구워 둔 값을 화면에서 한 번 더 맞춰 주는 역할입니다. 쿼리로 들어오는
 * 옛 주소(lesson.html?l=…)에서는 이쪽이 유일한 머리말이 됩니다.
 */

import { LANGS, BASE, homePath, allPath, coursePath, lessonPath } from './i18n.js';

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
  /* 구운 <head> 에 이미 같은 것이 있으면 갈아 끼웁니다. 새로 붙이면 canonical 이
     두 개가 되어 검색엔진이 무엇을 믿을지 알 수 없게 됩니다. */
  const sel = extra?.hreflang
    ? `link[rel="${ rel }"][hreflang="${ extra.hreflang }"]`
    : `link[rel="${ rel }"]`;
  const el = document.head.querySelector( sel ) || document.head.appendChild(
    Object.assign( document.createElement( 'link' ), { rel } ) );
  el.rel = rel;
  el.href = href;
  if ( extra ) { Object.entries( extra ).forEach( ( [ k, v ] ) => el.setAttribute( k, v ) ); }
}

/** 검색 결과에서 잘리지 않게 자릅니다. 한국어는 글자당 폭이 커서 기준이 다릅니다. */
function clamp( s, lang ) {
  const max = ( lang === 'ko' || lang === 'ja' ) ? 90 : 158;
  /* 원고에 <b> 가 섞여 있으면 태그가 그대로 미리보기에 실립니다. */
  s = String( s || '' ).replace( /<[^>]+>/g, '' ).replace( /\s+/g, ' ' ).trim();
  return s.length <= max ? s : s.slice( 0, max - 1 ).replace( /[\s,·]+$/, '' ) + '…';
}

/**
 * @param {object} o
 *   lang, title, desc, path   — 완성된 경로 ('/l/static-2')
 *   alt                       — 언어 코드를 받아 그 언어판 경로를 돌려주는 함수
 *   image                     — og/v2/<lang>/<이름>.jpg 의 이름 — 확장자 없이 (언어 폴더와 판은 여기서 붙입니다)
 *   jsonld                    — 구조화 데이터 객체(또는 배열)
 */
export function applySeo( o ) {
  const { lang, title, desc, path, image, keywords, jsonld, alt } = o;
  const d = clamp( desc, lang );

  document.title = title;
  meta( 'name', 'description', d );
  if ( keywords ) { meta( 'name', 'keywords', keywords ); }

  const url = ORIGIN + path;
  // 공유 이미지는 언어별로 굽습니다 (tools/make-og.py). 경로 규칙이 셋에 흩어져
  // 있으니 — 여기 · bake-head.py · make-og.py — 하나를 고치면 셋 다 고쳐야 합니다.
  const img = ORIGIN + '/og/v2/' + lang + '/' + ( image || 'default' ) + '.jpg';

  link( 'canonical', url );

  /* hreflang — 같은 문서의 다른 언어판을 서로 알려 줍니다.
     이게 없으면 네 언어판이 서로 중복 문서로 취급될 수 있습니다. */
  LANGS.forEach( l => link( 'alternate', ORIGIN + alt( l.code ), { hreflang: l.htmlLang } ) );
  link( 'alternate', ORIGIN + alt( BASE ), { hreflang: 'x-default' } );

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
    const s = document.head.querySelector( 'script[type="application/ld+json"]' )
      || document.head.appendChild( Object.assign( document.createElement( 'script' ),
        { type: 'application/ld+json' } ) );
    s.textContent = JSON.stringify( jsonld );
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
      target: { '@type': 'EntryPoint', urlTemplate: ORIGIN + allPath( BASE ) + '?q={search_term_string}' },
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
    url: ORIGIN + coursePath( c.id, lang ),
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
    url: ORIGIN + lessonPath( meta_.id, lang ),
    inLanguage: lang,
    isAccessibleForFree: true,
    learningResourceType: 'interactive simulation lesson',
    educationalLevel: 'secondary education',
    timeRequired: 'PT' + meta_.min + 'M',
    teaches: course.title,
    isPartOf: { '@type': 'Course', name: course.title, url: ORIGIN + coursePath( course.id, lang ) }
  }, {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Nudge', item: ORIGIN + homePath( lang ) },
      { '@type': 'ListItem', position: 2, name: course.title, item: ORIGIN + coursePath( course.id, lang ) },
      { '@type': 'ListItem', position: 3, name: L.title }
    ]
  } ];
}
