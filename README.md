"# first-langchain-app" 

Esta aplicación es una introducción a las aplicaciones basadas en LLM. El funcionamiento consiste en a partir de un nombre y apellido, se busca de forma automática su perfil de LinkedIn y Twitter mediante los cuales se extrae un resumen de la persona y se proporcionan 2 hechos interesantes de la persona.

Las fases del programa son los siguientes:

1.- A partir de un nombre completo (nombre y apellido) se llaman a dos ReAct Agents, uno para obtener la url del perfil de LinkedIn y otro para el perfil de Twitter.

2.- A partir de las urls obtenidas se scrapea la información de dichas páginas

3.- Con la información obtenida de la persona se llama al LLM para que haga un resumen y cuente dos hechos interesantes de la persona

4.- Se parsea la respuesta en un objeto de tipo diccionario con dos claves "summary" y "facts".

** Los ReAct Agents realizan las acciones de nuestra parte teniendo que proporcionarles la herramienta para poder buscar información en un navegador (tavily). Hasta que no encuentre una url que tenga sentido no parará de buscar la página correspondiente.