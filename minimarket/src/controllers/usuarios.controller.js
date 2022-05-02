import { Prisma } from "../prisma.js";
import { usuarioRequestDTO, loginRequestDTO } from "../dtos/usuarios.dtos.js";
import {compare, compareSync, hashSync} from 'bcrypt' // hashSync es syncrono y hash es una promesa 'await'
import jsonwebtoken from "jsonwebtoken"

export const crearUsuario =async (req, res)=>{
    try{
        const data = usuarioRequestDTO(req.body)
        hashSync(data.password,10) // aqui pide la contraseña y el nro de vueltas
        const password = hashSync(data.password,10)

        const nuevoUsuario = await Prisma.usuario.create({
            data: {...data, password},
            select:{
                id:true,
                nombre:true,
                email:true,
                rol:true,
                validado:true,
            } // aque cuando se registre un nuevo usuario no voy a mostrar/devolver la contraseña
        })//... los tres puntos es spread operator

        // ahora vamos a encriptar la contraseña. Aqui en Express lo tenemos que hacer desde cero.
        // Utilizaremos la libreria  bcrypt
        // una similitud en Flask en Python sería la libreria bcrypt
        // https://www.npmjs.com/package/bcrypt
        // En Django ya teniamos una libreria
        return res.status(201).json(nuevoUsuario);
    }   catch (error){
        // la clase error tiene el atributo message
        if (error instanceof Error) {
            return res.status(400).json({
                message:"error al crear el usuario",
                content: error.message,            
            })  
        }
        // typeof error instance        
    }
}
// PRIMERO HAREMOS EL LOGIN Y LUEGO EL ENVIO DE CORREOS
export const login =async(req, res)=>{
    // aqui requeriré el correo y la contraseña
    try {
        const data = loginRequestDTO(req.body)
        // buscar el usuario en la bd que tenga ese correo
        const usuarioEncontrado = await Prisma.usuario.findUnique({
            where:{ email: data.email},
            rejectOnNotFound:true
        })

        // validar su password
        if (compareSync(data.password, usuarioEncontrado.password)) {
            const token = jsonwebtoken.sign(
                {
                id:usuarioEncontrado.id, 
                mensaje:'API de minimarket',
                }, 
                'llave_secreta',
                {expiresIn:"1h" }
            ) // aqui creamos la token. Expira en 60 segundos o '60' 60 milisegundos

            return res.json({
                message:'bienvenido',
                content: token
            })
        } else {
            // si no es la password emitiré un error
            // raise new Exception('credenciales incorrectas')
            throw new Error('credencialees incorrectas') // new Error es lo mismo que decir Error
        }
    }   catch (error){
        if (error instanceof Error) {
            return res.status(400).json({
                message:'error al hacer el inicio de sesion',
                content: error.message,
            })
        }
        }
}