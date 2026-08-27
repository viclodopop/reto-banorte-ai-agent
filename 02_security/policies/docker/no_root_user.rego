package docker.security

# Regla: Denegar si el Dockerfile no tiene la instrucción USER
# Esto previene escalamiento de privilegios en el clúster bancario.
deny[msg] {
    not user_specified
    msg := "Seguridad Crítica: El Dockerfile debe especificar un usuario no-root (PoLP)."
}

user_specified {
    input[i].Cmd == "user"
}