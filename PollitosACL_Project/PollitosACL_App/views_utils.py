def calcular_acl(usuario, archivo,modelo):
    nivel_sujeto = usuario.nivel()
    nivel_objeto = archivo.nivel()

    if modelo == "bell":
        puede_leer = nivel_sujeto >= nivel_objeto  # No Read Up
        puede_escribir = nivel_sujeto <= nivel_objeto  # No Write Down
    elif modelo == "biba":
        puede_leer = nivel_sujeto <= nivel_objeto  # No Read Down
        puede_escribir = nivel_sujeto >= nivel_objeto  # No Write Up
    else:
        puede_leer = puede_escribir = False

    return puede_leer, puede_escribir

