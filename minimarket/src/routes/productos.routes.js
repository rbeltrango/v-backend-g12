import { Router } from "express";
import { crearProducto } from "../controllers/productos.controller.js";

export const productoRouter = Router()
productoRouter.post('/productos', crearProducto)
