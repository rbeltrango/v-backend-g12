// usando ECMAScript
import express from 'express'
import cors from "cors";
// usando CommonJs
// const express = require('express')

const servidor=express()
// middleware: es un intermediario que permite visualizar información adicional
// ahora podremos recibir y entender a un formato JSON
servidor.use(express.json())
// ahora puede recibir texto puro|recibir y entender los body que sean puro texto
servidor.use(express.raw())
servidor.use(express.urlencoded({extended:true}))
// el metodo GET  siempre va ser accedido a pesar que solamente en el methods le indiquemos otro
servidor.use(
    cors({
    origin: ["http://127.0.0.1"], 
    methods:["POST","PUT", "DELETE"],
    allowedHeaders:["Content_Type", "Authorization"],
})
);

const productos = [{
    nombre:'platano',
    precio:1.80,
    disponible:true
}]

// creando nuestro primer endpoint 
// cuando se ingrese a la ruta URL/  en el método GET
servidor.get('/', (req, res)=>{
    return res.status(200).json({
        message:'Bienvenido a mi API de productos'
    })
})

servidor.post('/productos',(req, res)=>{
    // mostrará todo el body enviado por el cliente
    console.log(req.body);
    const data=req.body

    productos.push(data)

    return res.status(201).json({
        message:'Producto agregado exitosamente'
    })
})

servidor.get('/productos', (req, res)=>{
    const data=productos
    return res.json({
        data // que la lave sera el mismo nombre dque la vatiable y su valro sera el contenido de esa variable
    })
})

servidor
    .route("/producto/:id")
    .get((req, res)=>{
    console.log(req.params);
    const {id} = req.params

    if (productos.length<id){
        // 400 > bad request (mala solicitud)
        return res.status(400).json({
            message:'El producto no existe'
        })
    }
    else{
        const data =productos[id-1]
    
    return res.json({
        data
    })
    }
})
// PUT
    .put((req, res)=>{
    // extraer el id
    const {id}=req.params
    // validar si existe esa poscicion en el arrgelo
    if (productos.length < id){
        return res.status(400).json({
            // si no existe, emitir un 400 indicando que el producto a actualizar no existe
            message:'El producto a actualizar no existe'
        })
    }else{
        // si existe, modficar con el body
        productos[id-1]=req.body

        return res.json({
            message:'Producto actualizado exitosamente',
            content: productos[id-1]
        })
    }
})
.delete((req, res)=>{
    const {id}=req.params
    if(productos.length<id){
        return res.json({
            message:'Producto a eliminar no existe'
        })

    }else{
        // metodo de los arreglos para eliminar uno o mas elementos del areglo iniciando desde una 
        //posicion e indicando la cantidad de elemntos a eliminar
        productos.splice(id-1,1);
        return res.json({
            message:'Producto eliminado exitosamente'
        });
    }
});  


servidor.listen(3000, () =>{
    console.log('Servidor corriendo exitosamente en el puerto 3000');
});
