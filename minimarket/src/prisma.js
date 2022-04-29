import prisma from '@prisma/client' // la libriria que empieza con @prisma indica que le pertenece prisma

const {PrismaClient}=prisma;

export const Prisma = new PrismaClient({});
