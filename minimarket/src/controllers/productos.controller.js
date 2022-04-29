import {Prisma} from '../prisma.js'

export const crearProducto =async (req, res)=>{
    console.log('me ejecuto primero');
    // con el await le estamos diciendo que a la promesa la vamos a esperar y tiene que ser exitoso
    try{
        const nuevoProducto= await Prisma.producto.create({data:req.body});
        console.log(nuevoProducto);

        console.log("yo me ejecuto al ultimo");

        return res.json({
            message:"Producto agregado exitosamente",
            content:nuevoProducto
        })
    }catch(e){
    console.log(e)
    return res.json({
        message:"error al crear el producto",
     })
    }
}
export const ListarProductos=async (req, res)=>{
    const productos=await Prisma.producto.findMany({})

    return res.json({
        content:productos,
    })
}

export const actualizarProducto=async(req,res)=>{
    const {id}=req.params
   
    // findunique > solamente podremos utilizar las columnas unique en la tabla, si
    // queremos hacer elfilgro por alguna columan que nosea 'unique entocnes usaresmos el findFirst()
    // inclusive usar operacdores como AND y OR
    // await Prisma.producto.findFirst({where:{}})    
    try{
        const productoEncontrado=await Prisma.producto.findUnique({
            where:{id:+id}, //el + convierte a numero
            rejectOnNotFound:true,
        })
        console.log(productoEncontrado)

        const productoActualizado=await Prisma.producto.update({
            data:req.body, 
            where:{id:productoEncontrado.id}
        })

        return res.json({
            message:"Producto actualizado exitosamente",
            content:productoActualizado,
        })
    } catch (e){
        console.log(e)
        return res.json({
            message:"error al actualizar el producto"
        })
    }
}

export const eliminarProducto=async(req,res)=>{
    const{id}=req.params

    try{
        // SELECT id FROM productos WHERE id = '...'
        const productoEncontrado=await Prisma.producto.findUnique({
            where:{id:Number(id)},
            select: {id:true},
        })
        await Prisma.producto.delete({where:{id:productoEncontrado.id}})

        return res.json({
            message:'producto eliminado exitosamente'
        });
    } catch (error){
        return res.json({
            message:'error al eliminar el producto'
        })
    }
}
