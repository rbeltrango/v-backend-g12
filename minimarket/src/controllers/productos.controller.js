import {Prisma} from '../prisma.js'

export const crearProducto =async (req, res)=>{
    console.log('me ejecuto primero');
    // con el await le estamos diciendo que a la promesa la vamos a esperar y tiene que ser exitoso
    try{
        const resultado= await Prisma.producto.create({data:req.body});
        console.log(resultado);

        console.log("yo me ejecuto al ultimo");

        return res.json({
            message:"Producto agregado exitosamente",
        })
    }catch(e){
    console.log(e)
    return res.json({
        message:"error al crear el producto",
     })
    }
}
