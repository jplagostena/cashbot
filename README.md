# Telegram Cashbot [![build-status](https://github.com/jplagostena/cashbot/actions/workflows/python-package.yml/badge.svg)](https://github.com/jplagostena/cashbot/actions/workflows/python-package.yml)

## ¿Qué hace?

Con mi concubina llevamos las cuentas de la casa en una spreadsheet de Google y siempre nos olvidábamos de cargar gastos. Este bot nace desde esa necesidad de poder cargarlo desde el celular, sin entrar a la planilla.

## Instalación

[Instalar virtual env](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

`pip install -r requirements.txt`

### ¿Cómo hago mi propio bot?

Te va a venir muuy bien leer este artículo de Telegram

[Bots: An introduction for developers](https://core.telegram.org/bots)

Ahi vas a descular:

- Como dar de alta un bot propio
- Como hacer la movida para que te aparezcan los comandos disponibles y su descripción

### ¿Cómo lo linkeo con Google?

Dos pasos:

1) Primero, vas a tener que declarar una app propia (esto se puede leer [acá](https://developers.google.com/identity/protocols/OAuth2)) y luego bajar los permisos a un archivo `creds.json` para que este bicho lo pueda leer.
2) Le vas a tener que dar permisos de tu cuenta de Google a esa app que vos creaste. Eso se hace con el comando `/autorizar`
3) En el `config.py` hay que poner el ID de tu spreadsheet

### Archivo de configuración

No la tengo muy atada en Python por lo que por ahora la config es medio manual. Hice un archivo `config_template.py` que si lo renombras a `config.py` ya la magia está hecha (y claro, también tenés que poner tu data)

### Troubleshooting

#### El bot en grupos

Por cuestiones de privacidad de Telegram, cuando el bot está en grupos y querés responderle, tenés que mencionar el mensaje que él envio antes. Si no, lo ignora, nunca entra en el handler.

Más info acá https://core.telegram.org/bots#privacy-mode

### Quiero tirarte un par de mejoras, ¿qué se puede hacer?

Mi intención es hacer tests de unidad, porque medio que lo empecé a los ponchazos, como una prueba estúpida y ahora ya tiene algo de lógica que vale la pena testear. Si, no fui muy TDD, pero estaba ansioso y era muy fácil de probar.

- [ ] Agarrar algún issue que está subido
- [ ] Tests de unidad
- [ ] Repasar TODOs
- [X] Una vez que haya algún test, subirlo a un CI  
- [ ] Si alguien la tiene clara con oauth y ve que se puede mejorar, chiflen. El comando `/autorizar` fue hecho con amor, pero sin mucho know-how y con algo de apuro.  
