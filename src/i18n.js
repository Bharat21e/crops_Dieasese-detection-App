// src/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LocizeBackend from 'i18next-locize-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(LocizeBackend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    backend: {
      projectId: 'b77ce5dc-69d5-4009-a4cf-7d9d6ae6f052',
      apiKey: 'cf7f413d-2737-4be3-af2b-d498c67ba732',
      referenceLng: 'en',
    },
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
