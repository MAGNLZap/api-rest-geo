export interface ComplementoServicio {
  sourceId: string
  title: string
  text: string
}
export interface RedaccionServicio {
  short: string
  description: string
  who: string
  access: string
  important?: string
  asesorIds?: string[]
  complements?: ComplementoServicio[]
}

export const fechaRedaccion = '2026-11-25'
export const redaccion: Record<string, RedaccionServicio> = {
  cdi: {
    short: 'Cuidado y desarrollo infantil para niñas y niños de 1 a 3 años.',
    description: 'Los Centros de Desarrollo Infantil ofrecen atención para el cuidado y desarrollo de niñas y niños pequeños. Puedes consultar sus ubicaciones y solicitar orientación sobre el ingreso.',
    who: 'Familias con niñas y niños de 1 a 3 años, de acuerdo con los criterios de acceso del servicio.',
    access: 'Consulta con la institución los requisitos de ingreso y la disponibilidad de atención. Encontrar un centro en el mapa no confirma que tenga cupos.',
    important: 'El permiso de funcionamiento es un trámite para quienes operan centros, no un requisito de ingreso que deba tramitar una familia.',
  },
  cnh: {
    short: 'Acompañamiento familiar durante la gestación y para familias con niñas y niños de 0 a 3 años.',
    description: 'Creciendo con Nuestros Hijos acompaña a las familias en la etapa de gestación y en los primeros años de vida de niñas y niños. Su finalidad es el acompañamiento familiar, no la entrega de un bono.',
    who: 'Gestantes y familias con niñas y niños de 0 a 3 años, según las condiciones del servicio.',
    access: 'Consulta cómo recibir acompañamiento familiar en tu territorio y cuáles son las condiciones para vincularte al servicio.',
  },
  adulto: {
    short: 'Cuidado y atención a personas mayores mediante servicios residenciales, diurnos, domiciliarios y espacios de encuentro.',
    description: 'Reúne distintas formas de atención: cuidado residencial, atención durante el día, atención en el domicilio y espacios de encuentro. La orientación permite conocer qué modalidad consultar según la situación de la persona.',
    who: 'Personas de 65 años o más, de acuerdo con las condiciones de acceso de cada modalidad.',
    access: 'Solicita orientación sobre la modalidad de atención y el punto al que debes acudir. Consulta los requisitos y la disponibilidad antes de iniciar el ingreso.',
    important: 'La atención y el cuidado no equivalen a una pensión económica; cada servicio tiene su propia finalidad y condiciones.',
  },
  discapacidad: {
    short: 'Atención a personas con discapacidad en centros diurnos, acogida inclusiva, el hogar y la comunidad.',
    description: 'Comprende atención en centros diurnos, centros de acogida inclusiva y acompañamiento en el hogar y la comunidad. La modalidad y las condiciones de acceso deben consultarse para cada situación.',
    who: 'Personas con discapacidad que cumplen los criterios de atención de la modalidad correspondiente.',
    access: 'Solicita información sobre las modalidades y la valoración que corresponda. La institución debe verificar las condiciones de atención.',
    important: 'No deben aplicarse a estos servicios los requisitos de un bono o una pensión: son apoyos diferentes.',
  },
  proteccion: {
    short: 'Atención especializada y orientación ante situaciones de vulneración de derechos.',
    description: 'Protección especial atiende situaciones de vulneración de derechos de niñas, niños, adolescentes y otras personas en situación de vulnerabilidad. Algunos casos requieren derivación o medidas de protección.',
    who: 'Niñas, niños, adolescentes y otras personas en situación de vulnerabilidad, según la situación y el servicio de protección.',
    access: 'Busca orientación institucional para conocer el procedimiento y la instancia competente. Algunos casos requieren derivación o medidas de protección; este formulario no las emite.',
    important: 'Que aparezca el Bono de orfandad entre las opciones del formulario no significa que toda situación de protección corresponda a ese beneficio.',
  },
  adopcion: {
    short: 'Información y orientación para iniciar procesos de adopción nacional o internacional.',
    description: 'El piloto reúne orientación sobre adopción nacional e internacional. Como complemento, Asesor593 describe la solicitud de adopción nacional de niñas, niños y adolescentes con declaratoria de adoptabilidad y la evaluación de idoneidad de las personas solicitantes.',
    who: 'Personas interesadas en iniciar un proceso de adopción. La ficha complementaria de adopción nacional se dirige a personas naturales ecuatorianas.',
    access: 'Para adopción nacional, la ficha indica contactar a la Unidad Técnica de Adopciones zonal para la entrevista inicial y orientación sobre formación, solicitud y evaluación. Para adopción internacional, consulta las instancias y requisitos específicos.',
    important: 'Iniciar la solicitud no garantiza una asignación. Los documentos deben confirmarse según la etapa; la ficha de adopción nacional no acredita los requisitos de adopción internacional.',
    asesorIds: ['solicitud-de-adopcion-nacional-de-ninas-ninos-y-adolescentes-con'],
  },
  credito: {
    short: 'Financiamiento para emprendimientos dirigido a personas usuarias de determinadas transferencias monetarias.',
    description: 'El Crédito de Desarrollo Humano orienta sobre acceso a financiamiento para emprendimientos, conforme a las condiciones del programa. No es lo mismo que recibir formación o participar en actividades de apoyo productivo.',
    who: 'Personas usuarias de determinadas transferencias monetarias que cumplen las condiciones del programa.',
    access: 'Consulta si la transferencia que recibes y tu situación corresponden a las condiciones del programa, y cómo iniciar la solicitud. Esta orientación no aprueba un crédito.',
  },
  bonos: {
    short: 'Información sobre bonos y pensiones: apoyos económicos con condiciones específicas para cada prestación.',
    description: 'Son transferencias monetarias no contributivas. Cada bono o pensión tiene una población destinataria y un mecanismo de acceso propios; no son prestaciones intercambiables.',
    who: 'Personas y familias que cumplen las condiciones establecidas para la transferencia correspondiente.',
    access: 'Consulta la ficha de la prestación que te interesa. Las fichas de BDH, BDHV, Bono 1000 días y las dos pensiones describen procesos de habilitación; no todas las transferencias admiten una solicitud directa.',
    important: 'Los montos y condiciones que se resumen aquí corresponden a las fichas consultadas el 24/11/2026. Confirma su vigencia con la institución. La acreditación bancaria es una forma de pago, no un formulario de inscripción.',
    complements: [
      {
        sourceId: 'bono-desarrollo-humano',
        title: 'Bono de Desarrollo Humano (BDH)',
        text: 'La ficha describe una transferencia de USD 55 mensuales para hogares en pobreza, pobreza extrema o vulnerabilidad. La habilitación se realiza según las condiciones del programa; no es una inscripción libre en este formulario.',
      },
      {
        sourceId: 'bono-desarrollo-humano-variable',
        title: 'Bono de Desarrollo Humano con componente variable (BDHV)',
        text: 'Beneficio para madres de familia con hijos menores de 18 años en pobreza o pobreza extrema; la ficha de destinatarios enfatiza extrema pobreza. Publica valores relacionados con la edad y número de hijos, pero no una fórmula completa para calcular el pago.',
      },
      {
        sourceId: 'bono-mil-dias',
        title: 'Bono 1000 días',
        text: 'Ayuda económica durante el embarazo y para niñas y niños menores de 2 años de hogares en pobreza o extrema pobreza, que contribuye a prevenir la desnutrición crónica infantil.',
      },
      {
        sourceId: 'pension-mejores-an',
        title: 'Pensión Mis Mejores Años',
        text: 'La ficha publica una ayuda de USD 100 mensuales para personas adultas mayores en pobreza o pobreza extrema, según el Registro Social y las condiciones de habilitación.',
      },
      {
        sourceId: 'pension-toda-una-vida',
        title: 'Pensión Toda Una Vida',
        text: 'La ficha publica una ayuda de USD 100 mensuales para personas menores de 65 años con discapacidad de al menos 40 %, registrada ante el MSP, en pobreza o extrema pobreza y sujetas a las condiciones de habilitación.',
      },
      {
        sourceId: 'bono-joaquin-gallegos',
        title: 'Bono Joaquín Gallegos Lara',
        text: 'La ficha publica una ayuda de USD 240 mensuales para contribuir a la atención y cuidado de personas con discapacidad que cumplen las condiciones del programa y requieren un cuidador. Tiene una ficha propia en este catálogo.',
      },
    ],
  },
  contingencia: {
    short: 'Orientación sobre la cobertura de contingencias ante calamidades que afectan el sustento o la vivienda familiar.',
    description: 'Esta opción orienta a familias afectadas por calamidades sobre la cobertura de contingencias y la verificación de su caso, conforme a la normativa aplicable.',
    who: 'Familias afectadas por calamidades que comprometen su sustento o vivienda, sujetas a valoración y normativa vigente.',
    access: 'Consulta con la institución el procedimiento de solicitud y la información que se requiere para verificar el caso.',
  },
  jovenes: {
    short: 'Información sobre procesos de atención, formación y desarrollo para jóvenes.',
    description: 'Reúne orientación sobre las opciones de atención y formación dirigidas a jóvenes. La participación depende de los criterios y mecanismos de inscripción de cada convocatoria.',
    who: 'Jóvenes de 18 a 29 años, conforme a los criterios de acceso de cada opción.',
    access: 'Consulta las convocatorias vigentes y sus mecanismos de inscripción antes de iniciar una solicitud.',
  },
  emprendimiento: {
    short: 'Formación y apoyo para fortalecer capacidades y participar en oportunidades de vinculación productiva.',
    description: 'Se orienta al fortalecimiento de capacidades y la vinculación productiva de la población objetivo de los programas de inclusión económica. No equivale a la aprobación de un crédito.',
    who: 'Personas que forman parte de la población objetivo de los programas de inclusión económica.',
    access: 'Consulta las opciones de formación y apoyo disponibles, sus condiciones de participación y cómo vincularte.',
  },
  orfandad: {
    short: 'Información sobre el Bono de orfandad para niñas, niños y adolescentes en los casos previstos para esta prestación.',
    description: 'Orienta sobre la prestación, la solicitud y los documentos correspondientes a los casos de orfandad previstos por el programa. La aprobación requiere verificación institucional.',
    who: 'Niñas, niños y adolescentes que cumplen los requisitos específicos de la prestación.',
    access: 'Consulta las condiciones del beneficio, cómo presentar la solicitud y qué documentos se requieren. La institución verificará el caso antes de aprobarlo.',
    important: 'No es un proceso de adopción ni una ayuda que se conceda automáticamente por seleccionar una opción de protección.',
  },
  sustituto: {
    short: 'Orientación sobre la certificación de sustituto por solidaridad humana para el cuidado de personas con discapacidad.',
    description: 'Esta opción informa sobre un procedimiento de certificación relacionado con el cuidado de personas con discapacidad. No es un bono ni una pensión.',
    who: 'Personas que cumplen las condiciones legales del procedimiento de certificación.',
    access: 'Consulta los requisitos de la certificación y el trámite que corresponde a tu situación.',
  },
  bjl: {
    short: 'Ayuda económica mensual para contribuir al cuidado de personas con discapacidad que requieren un cuidador, según las condiciones del programa.',
    description: 'El Bono Joaquín Gallegos Lara contribuye a la atención y cuidado de personas con discapacidad que requieren asistencia permanente. La ficha de Asesor593 consultada publica una ayuda de USD 240 mensuales. El piloto también contempla orientación sobre acceso y acompañamiento técnico para las personas beneficiarias. El beneficio no se concede por completar este formulario.',
    who: 'Personas con discapacidad que cumplen las condiciones específicas descritas en la ficha consultada y requieren un cuidador.',
    access: 'La ficha indica verificar las condiciones de discapacidad y Registro Social, acudir personalmente a un Balcón de Servicio y presentar la cédula original para la inscripción. Consulta quién debe comparecer cuando la persona requiere cuidador.',
    important: 'La captura del 24/11/2026 no precisa el porcentaje de discapacidad exigido. Confirma los requisitos y el monto vigentes con la institución; no debe trasladarse aquí el porcentaje de otra pensión.',
    asesorIds: ['bono-joaquin-gallegos'],
  },
  ciudadania: {
    short: 'Orientación para solicitar información pública y certificaciones de documentos institucionales.',
    description: 'Atención ciudadana y certificaciones reúne consultas de información pública y solicitudes de certificación de documentos de la institución.',
    who: 'Ciudadanía y organizaciones que requieren información o certificaciones de documentos institucionales.',
    access: 'Presenta tu solicitud por los canales institucionales vigentes y consulta el procedimiento correspondiente al documento o información que necesitas.',
  },
  organizaciones: {
    short: 'Asesoría, legalización y registro de organizaciones sociales sin fines de lucro.',
    description: 'Orienta a las organizaciones sociales y sus representantes sobre los procedimientos de asesoría, legalización y registro que correspondan.',
    who: 'Organizaciones sociales sin fines de lucro y sus representantes.',
    access: 'Consulta el trámite específico de la organización y la documentación que se requiere para realizarlo.',
  },
  permisos: {
    short: 'Información sobre la autorización de funcionamiento de unidades de atención y los trámites de sus responsables.',
    description: 'Los permisos de funcionamiento se dirigen a quienes son responsables de operar unidades de atención. Como referencia específica, Asesor593 describe el permiso para brindar atención en Centros de Desarrollo Infantil de 1 a 3 años, de administración directa, por convenio, privados y fiscomisionales.',
    who: 'Responsables de unidades sujetas a permiso. La ficha de CDI incluye personas naturales ecuatorianas o extranjeras y personas jurídicas públicas o privadas.',
    access: 'Consulta el procedimiento y los documentos según el tipo de unidad. Para CDI, la ficha describe la preparación y presentación de la solicitud ante la dirección distrital, una inspección coordinada y el retiro del permiso en la instancia correspondiente.',
    important: 'No es un trámite de matrícula o ingreso de una niña o niño. Los requisitos del permiso CDI no deben aplicarse automáticamente a otras unidades o modalidades.',
    asesorIds: ['otorgamiento-de-permisos-de-funcionamiento-para-centros-de-desar'],
  },
  acompanamiento: {
    short: 'Acompañamiento familiar para familias usuarias del Bono de Desarrollo Humano con componente variable.',
    description: 'Este servicio ofrece acompañamiento a familias vinculadas al Bono de Desarrollo Humano con componente variable. El acompañamiento y la transferencia económica son prestaciones distintas.',
    who: 'Familias usuarias del Bono de Desarrollo Humano con componente variable vinculadas al programa.',
    access: 'Consulta con la institución cómo se realiza la vinculación al acompañamiento familiar. El mecanismo concreto debe confirmarse; no se inicia por completar este formulario.',
  },
}
