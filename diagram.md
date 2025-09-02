flowchart LR
%% ============================================================
%% PoC Rappi Business - Arquitectura + Flujo
%% ============================================================

%% -------------------- Arquitectura --------------------
subgraph UserHost [Host de Ejecución - Dev Server]
  direction TB

  subgraph Scripts [Scripts Python]
    A1[login_and_save_session.py]
    A2[send_dm.py]
  end

  subgraph Secrets [Secrets Entorno]
    S1[(IG_USERNAME)]
    S2[(IG_PASSWORD)]
  end

  subgraph State [Persistencia]
    F1[(session.json)]
    L1[[Logs y Errores]]
  end

  subgraph Controls [Controles Operativos]
    R1[[Rate Limiter <br/> Delays aleatorios]]
    P1[[Proxy estatico o residencial]]
    M1[[Monitor y Alertas]]
  end
end

subgraph InstagramSide [Instagram Infra Remota]
  IGAPI[[API Privada de Instagram]]
  IGAuth[[Autenticacion 2FA]]
end

%% -------------------- Relaciones de Arquitectura --------------------
A1 --- F1
A2 --- F1
A1 --- IGAuth
A2 --- IGAPI
A1 --- S1
A1 --- S2
A2 --- S1
A2 --- S2
A1 --- L1
A2 --- L1
R1 -.-> A2
P1 -.-> A1
P1 -.-> A2
M1 -.-> L1

%% -------------------- Flujo login_and_save_session.py --------------------
subgraph FlowLogin [Flujo login_and_save_session.py]
  FL0([Inicio])
  FL1{Credenciales en entorno?}
  FL2[Prompt usuario y password]
  FL3[Instanciar Client]
  FL4[Login basico con usuario y password]
  FL5{Requiere 2FA?}
  FL6[Solicitar codigo 2FA]
  FL7[Login con verification code]
  FL8[Guardar session.json]
  FL9([Fin OK])
  FLerr[[Error en login → log]]

  FL0 --> FL1
  FL1 -- No --> FL2 --> FL3
  FL1 -- Si --> FL3
  FL3 --> FL4 --> FL5
  FL5 -- Si --> FL6 --> FL7 --> FL8 --> FL9
  FL5 -- No --> FL8 --> FL9
  FL4 -- Error --> FLerr
  FL7 -- Error --> FLerr
end

%% -------------------- Flujo send_dm.py --------------------
subgraph FlowSend [Flujo send_dm.py]
  FS0([Inicio])
  FS1{Existe session.json?}
  FS2[Instanciar Client]
  FS3[Cargar settings de session.json]
  FS4[Refrescar login con password]
  FS5[Login nueva sesion]
  FS6[Guardar session.json]
  FS7{Args validos?}
  FS8[Obtener user_id desde username]
  FS9[Enviar mensaje directo]
  FS10([Fin OK])
  FSerr1[[Error sesion → log]]
  FSerr2[[Error username → log]]
  FSerr3[[Error envio DM → log]]

  FS0 --> FS2 --> FS1
  FS1 -- Si --> FS3 --> FS4
  FS4 -- Error --> FSerr1
  FS1 -- No --> FS5 --> FS6
  FS5 -- Error --> FSerr1

  FS4 --> FS7
  FS6 --> FS7
  FS7 -- No --> FSerr1
  FS7 -- Si --> FS8
  FS8 -- Error --> FSerr2
  FS8 --> FS9
  FS9 -- Error --> FSerr3
  FS9 --> FS10
end
