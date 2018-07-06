from .ResponseHandlers import ResponseHandlers as EH

HL = {'connect': EH.connect, 'authorise': EH.authoreg, 'registration': EH.authoreg, 'message': EH.message, 'disconnect': EH.disconnect}
