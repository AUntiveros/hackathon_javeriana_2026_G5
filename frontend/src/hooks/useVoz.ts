import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * Voz del navegador (Web Speech API), voice-first para adulto mayor.
 * - hablar(): TTS es-ES pausado, con red de seguridad si onend nunca llega.
 * - escuchar(): STT SpeechRecognition; resuelve con el transcript.
 * Expone flags de soporte para degradar con gracia (typing fallback).
 */

// SpeechRecognition llega con prefijo webkit en Chrome/Android
const SpeechRecognitionImpl = window.SpeechRecognition ?? window.webkitSpeechRecognition;

export const sttSoportado = Boolean(SpeechRecognitionImpl);
export const ttsSoportado = 'speechSynthesis' in window;

export interface UseVoz {
  hablar: (texto: string, alTerminar: () => void) => void;
  escuchar: () => Promise<string>;
  cancelar: () => void;
  escuchando: boolean;
  sttSoportado: boolean;
  ttsSoportado: boolean;
}

export function useVoz(): UseVoz {
  const [escuchando, setEscuchando] = useState(false);
  const recRef = useRef<SpeechRecognitionInstance | null>(null);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  useEffect(
    () => () => {
      window.speechSynthesis?.cancel();
      recRef.current?.abort();
    },
    [],
  );

  const hablar = useCallback((texto: string, alTerminar: () => void) => {
    let terminado = false;
    const fin = () => {
      if (terminado) return;
      terminado = true;
      alTerminar();
    };
    // red de seguridad: si el TTS nunca dispara onend (sin voces es-ES,
    // navegador raro), la UI no se queda pegada
    setTimeout(fin, Math.max(4000, texto.length * 90));

    if (!ttsSoportado) return;
    const u = new SpeechSynthesisUtterance(texto);
    u.lang = 'es-ES';
    u.rate = 0.92; // pausado, amable
    u.pitch = 1.15;
    u.onend = fin;
    u.onerror = fin;
    utteranceRef.current = u; // iOS Safari: sin referencia viva, a veces se garbage-collecta a mitad de la frase

    window.speechSynthesis.cancel();
    // iOS Safari: speak() justo después de cancel() en el mismo tick a veces no suena;
    // un pequeño delay lo evita de forma confiable (bug conocido de WebKit)
    setTimeout(() => window.speechSynthesis.speak(u), 60);
  }, []);

  const escuchar = useCallback((): Promise<string> => {
    if (!SpeechRecognitionImpl) return Promise.resolve('');
    return new Promise((resolve) => {
      const rec = new SpeechRecognitionImpl!();
      recRef.current = rec;
      rec.lang = 'es-PE';
      rec.interimResults = false;
      rec.maxAlternatives = 1;

      let texto = '';
      rec.onresult = (e: SpeechRecognitionEvent) => {
        texto = e.results[0][0].transcript;
      };
      rec.onend = () => {
        setEscuchando(false);
        resolve(texto);
      };
      rec.onerror = () => {
        setEscuchando(false);
        resolve(texto);
      };
      setEscuchando(true);
      rec.start();
    });
  }, []);

  const cancelar = useCallback(() => {
    window.speechSynthesis?.cancel();
    recRef.current?.abort();
    setEscuchando(false);
  }, []);

  return { hablar, escuchar, cancelar, escuchando, sttSoportado, ttsSoportado };
}
