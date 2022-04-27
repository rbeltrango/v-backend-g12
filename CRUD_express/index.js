// usando ECMAScript
import express from 'express'
// usando CommonJs
// const express = require('express')

const servidor=express()
// middleware: es un intermediario que permite visualizar información adicional
// ahora podremos recibir y entender a un formato JSON
servidor.use(express.json())
// ahora puede recibir texto puro|recibir y entender los body que sean puro texto
servidor.use(express.raw())
servidor.use(express.urlencoded({extended:true}))

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

servidor.get('/producto/:id', (req, res)=>{
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
servidor.put('/producto/:id', (req, res)=>{
    // extraer el id
    const {id}=req.params
    // validar si existe esa poscicion en el arrgelo
    if (productos.length < id){
        return res.status(400).json({
            message:'El producto a actualizar no existe'
        })
    }else{
        productos[id-1]=req.body
        
        return res.json({
            message:'Producto actualizado exitosamente',
            content: productos[id-1]
        })
    }
})
    // si existe, modficar con el body
    // si no existe, emitir un 400 indicando que el producto a actualizar no existe


servidor.listen(3000, () =>{
    console.log('Servidor corriendo exitosamente en el puerto 3000')
})
