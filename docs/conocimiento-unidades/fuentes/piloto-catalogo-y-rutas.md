# Captura de contenido y rutas del piloto

Consulta: 2026-11-24.

Fuente: https://github.com/sgde-mtdh/Geoportal-MTDH/blob/36eec6664f38af0eb1dcd3c1f17aa79c65480468/servicios/index.html

SHA-256 del HTML consultado: `04c60f4393eaa06deef41dd2b9f5c1e64fd6205ae19201af45729cabbf7d299a`.

Extracción estática de los literales `services` y `paths`, sin ejecutar JavaScript remoto. Se omiten los iconos iniciales de las etiquetas de público; se conservan textos, identificadores, orden y asociaciones. No contiene estilos ni componentes gráficos.

```json
{
  "services": [
    {
      "id": "cdi",
      "title": "Centros de Desarrollo Infantil",
      "short": "Cuidado y desarrollo de niñas y niños de 1 a 3 años.",
      "who": "Familias con niñas y niños pequeños, según los criterios de acceso del servicio.",
      "access": "Solicita orientación para el ingreso. La institución verificará requisitos y disponibilidad.",
      "map": true
    },
    {
      "id": "cnh",
      "title": "Creciendo con Nuestros Hijos",
      "short": "Acompañamiento familiar para gestantes y niñas y niños de 0 a 3 años.",
      "who": "Gestantes y familias con niñas y niños pequeños.",
      "access": "Consulta cómo recibir acompañamiento en tu territorio."
    },
    {
      "id": "adulto",
      "title": "Atención a personas adultas mayores",
      "short": "Atención residencial, diurna, domiciliaria y espacios de encuentro.",
      "who": "Personas de 65 años o más, según las condiciones de acceso.",
      "access": "Consulta la modalidad más adecuada y el punto de orientación correspondiente."
    },
    {
      "id": "discapacidad",
      "title": "Atención a personas con discapacidad",
      "short": "Atención en centros diurnos, acogida inclusiva y en el hogar y comunidad.",
      "who": "Personas con discapacidad que cumplen los criterios de atención.",
      "access": "Solicita información sobre la modalidad y valoración correspondiente."
    },
    {
      "id": "proteccion",
      "title": "Protección especial",
      "short": "Atención especializada ante situaciones de vulneración de derechos.",
      "who": "Niñas, niños, adolescentes y otras personas en situación de vulnerabilidad.",
      "access": "Busca orientación institucional; algunos casos requieren derivación o medidas de protección."
    },
    {
      "id": "adopcion",
      "title": "Adopciones",
      "short": "Orientación sobre los procesos de adopción nacional e internacional.",
      "who": "Personas interesadas en iniciar el proceso de adopción.",
      "access": "Consulta los requisitos y las instancias de adopciones; el proceso requiere evaluación de idoneidad."
    },
    {
      "id": "credito",
      "title": "Crédito de Desarrollo Humano",
      "short": "Acceso a financiamiento para emprendimientos, conforme a requisitos.",
      "who": "Personas usuarias de determinadas transferencias monetarias que cumplen las condiciones del programa.",
      "access": "Consulta si cumples los requisitos y cómo iniciar la solicitud; no es una aprobación automática."
    },
    {
      "id": "bonos",
      "title": "Bonos y pensiones",
      "short": "Información sobre transferencias monetarias no contributivas.",
      "who": "Personas y familias que cumplen los criterios establecidos para cada transferencia.",
      "access": "Solicita información sobre condiciones y mecanismos de atención; no todas las transferencias se solicitan directamente."
    },
    {
      "id": "contingencia",
      "title": "Cobertura de contingencias",
      "short": "Orientación ante calamidades que afectan el sustento o vivienda familiar.",
      "who": "Familias afectadas, sujetas a valoración y normativa vigente.",
      "access": "Consulta el procedimiento de solicitud y verificación del caso."
    },
    {
      "id": "jovenes",
      "title": "Atención y formación para jóvenes",
      "short": "Procesos de formación y desarrollo dirigidos a jóvenes.",
      "who": "Jóvenes de 18 a 29 años, conforme a criterios de acceso.",
      "access": "Consulta convocatorias y mecanismos de inscripción vigentes."
    },
    {
      "id": "emprendimiento",
      "title": "Formación y apoyo para emprendimientos",
      "short": "Fortalecimiento de capacidades y vinculación productiva.",
      "who": "Población objetivo de los programas de inclusión económica.",
      "access": "Consulta opciones de formación y participación."
    },
    {
      "id": "orfandad",
      "title": "Bono de orfandad",
      "short": "Orientación sobre la prestación para niñas, niños y adolescentes en los casos previstos.",
      "who": "Niñas, niños y adolescentes que cumplen los requisitos específicos.",
      "access": "Consulta la solicitud y documentos requeridos; la aprobación está sujeta a verificación."
    },
    {
      "id": "sustituto",
      "title": "Certificación de sustituto por solidaridad humana",
      "short": "Información sobre la certificación prevista para el cuidado de personas con discapacidad.",
      "who": "Personas que cumplen las condiciones legales del procedimiento.",
      "access": "Consulta requisitos y trámite de certificación."
    },
    {
      "id": "bjl",
      "title": "Bono Joaquín Gallegos Lara",
      "short": "Orientación sobre acceso y acompañamiento técnico para beneficiarios.",
      "who": "Personas que cumplen las condiciones específicas del programa.",
      "access": "Consulta el proceso de solicitud y valoración."
    },
    {
      "id": "ciudadania",
      "title": "Atención ciudadana y certificaciones",
      "short": "Acceso a información pública y certificación de documentos institucionales.",
      "who": "Ciudadanía y organizaciones que requieren información o documentos.",
      "access": "Presenta la solicitud mediante los canales institucionales vigentes."
    },
    {
      "id": "organizaciones",
      "title": "Organizaciones sociales",
      "short": "Asesoría, legalización y registro de organizaciones sociales sin fines de lucro.",
      "who": "Organizaciones sociales y sus representantes.",
      "access": "Consulta el trámite específico y la documentación necesaria."
    },
    {
      "id": "permisos",
      "title": "Permisos de funcionamiento",
      "short": "Información sobre permisos para unidades de atención.",
      "who": "Responsables de unidades de atención sujetas a permisos.",
      "access": "Consulta los requisitos del procedimiento correspondiente."
    },
    {
      "id": "acompanamiento",
      "title": "Acompañamiento familiar",
      "short": "Acompañamiento a familias usuarias del Bono de Desarrollo Humano con componente variable.",
      "who": "Familias vinculadas al programa.",
      "access": "La modalidad de vinculación debe confirmarse institucionalmente."
    }
  ],
  "paths": [
    {
      "id": "infancia",
      "label": "Una niña o niño",
      "needs": [
        [
          "cuidado",
          "Cuidado y desarrollo infantil",
          [
            "cdi",
            "cnh"
          ]
        ],
        [
          "proteccion",
          "Necesita protección",
          [
            "proteccion",
            "orfandad"
          ]
        ],
        [
          "otra",
          "Quiero conocer otras ayudas",
          [
            "cdi",
            "cnh",
            "proteccion"
          ]
        ]
      ]
    },
    {
      "id": "mayor",
      "label": "Una persona mayor",
      "needs": [
        [
          "atencion",
          "Cuidado y actividades",
          [
            "adulto"
          ]
        ],
        [
          "dinero",
          "Apoyo económico",
          [
            "bonos"
          ]
        ],
        [
          "otra",
          "Quiero conocer opciones",
          [
            "adulto",
            "bonos"
          ]
        ]
      ]
    },
    {
      "id": "discapacidad",
      "label": "Una persona con discapacidad",
      "needs": [
        [
          "atencion",
          "Atención y acompañamiento",
          [
            "discapacidad"
          ]
        ],
        [
          "bono",
          "Información sobre bonos",
          [
            "bjl",
            "bonos"
          ]
        ],
        [
          "otra",
          "Otros apoyos",
          [
            "discapacidad",
            "sustituto"
          ]
        ]
      ]
    },
    {
      "id": "familia",
      "label": "Mi familia",
      "needs": [
        [
          "credito",
          "Empezar un negocio",
          [
            "credito",
            "emprendimiento"
          ]
        ],
        [
          "emergencia",
          "Una emergencia o calamidad",
          [
            "contingencia"
          ]
        ],
        [
          "bonos",
          "Bonos y pensiones",
          [
            "bonos"
          ]
        ],
        [
          "otra",
          "Apoyo familiar",
          [
            "acompanamiento",
            "cnh"
          ]
        ]
      ]
    },
    {
      "id": "proteccion",
      "label": "Alguien necesita protección",
      "needs": [
        [
          "derechos",
          "Se vulneraron sus derechos",
          [
            "proteccion"
          ]
        ],
        [
          "orfandad",
          "Bono de orfandad",
          [
            "orfandad"
          ]
        ],
        [
          "otra",
          "Necesito orientación",
          [
            "proteccion"
          ]
        ]
      ]
    },
    {
      "id": "otros",
      "label": "Otra ayuda",
      "needs": [
        [
          "adopcion",
          "Quiero adoptar",
          [
            "adopcion"
          ]
        ],
        [
          "joven",
          "Formación para jóvenes",
          [
            "jovenes",
            "emprendimiento"
          ]
        ],
        [
          "tramite",
          "Información o documentos",
          [
            "ciudadania",
            "organizaciones",
            "permisos"
          ]
        ],
        [
          "otra",
          "Ver todo el catálogo",
          []
        ]
      ]
    }
  ]
}
```
