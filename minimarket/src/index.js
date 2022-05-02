import express,{json} from 'express'
import {productosRouter} from './routes/productos.routes.js'
import { usuarioRouter } from './routes/usuarios.routes.js'
const app =express()

app.use(json())

// nullish coalesing operator
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_operator
// si el primer valor no es nulo o undefined, será ese valor, caso contrario tomará el segundo valor
const PORT = process.env.PORT ?? 3000;

app.get('/',(req,res)=>{
    res.json({
    message:"Bienvenido a mi API del minimarket"
})
})

app.use(productosRouter)
app.use(usuarioRouter)

app.listen(PORT, ()=>{
    // LA COMA invertida indica que hay una variable en el codigo javascript
    console.log(`Servidor corriendo exitosamente en el puerto ${PORT}`)
})

