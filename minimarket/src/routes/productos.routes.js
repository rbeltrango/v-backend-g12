import { Router } from "express";
import { 
    actualizarProducto,
    crearProducto, 
    eliminarProducto, 
    ListarProductos,
 } from "../controllers/productos.controller.js";

export const productosRouter = Router()

productosRouter.route('/productos').post(crearProducto).get(ListarProductos);
productosRouter
.route('/producto/:id')
.put(actualizarProducto)
.delete(eliminarProducto);
