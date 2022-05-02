import prisma from "@prisma/client"
import validator from "validator"

export function usuarioRequestDTO({nombre, email, password, rol}){  
    const errores =[]
    if(!validator.isEmail(email)){
        errores.push('El email no es un correo válido')
    }
    if (validator.isEmpty(password)){
    errores.push("el password no puede estar vacio")
    }
    if (validator.isEmpty(nombre)){
    errores.push("el nombre no puede estar vacio")
    }
    if (
        rol !== prisma.USUARIO_ROL.ADMINISTRADOR && // || indica o y && indica i
        rol !== prisma.USUARIO_ROL.CLIENTE
    ){
        errores.push(
        `El rol puede ser ${prisma.USUARIO_ROL.ADMINISTRADOR} o ${prisma.USUARIO_ROL.CLIENTE}`
        )
    }
    if (errores.length !=0){
        throw Error(errores);
    } else{
        return{
            nombre,
            email,
            password,
            rol,
        };
    }
}
// alt + 96 > `
// alt + 124 > |

export function loginRequestDTO({email, password}){
    // validar que el email sea un email y que la password no sea nula
    const errores =[]
    if(!validator.isEmail(email)){ //  "!validator.isEmail(email)" indica si no es un correo
        errores.push('El email no es un correo válido') 
    }
    if(validator.isEmpty(password)){ // "validator.isEmpty(password)" indica si esta vacia la contraseña
        errores.push("el password no puede estar vacio")
    }
    if (errores.length !=0){
        throw Error(errores)
    } else {
        return{
            email,
            password,
        }
    }
}
