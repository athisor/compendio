/**
 * Script para compilar packs de Foundry VTT usando classic-level directamente.
 * La CLI de Foundry (fvtt) tiene problemas con la creación de LevelDB.
 * Este script usa el mismo método que el sistema SWADE oficial.
 * 
 * Uso: node build-packs.js
 * Requisitos: npm install classic-level
 */

import { ClassicLevel } from 'classic-level';
import { existsSync, promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const srcDir = path.join(__dirname, 'src', 'packs');
const destDir = path.join(__dirname, 'packs');

// Packs a compilar (solo los que tienen contenido)
const itemPacks = ['iz3-edges', 'iz3-hindrances'];

async function main() {
  console.log('============================================================');
  console.log('Compilador de Packs para Foundry VTT (usando classic-level)');
  console.log('============================================================\n');

  // Crear directorio de destino si no existe
  if (!existsSync(destDir)) {
    await fs.mkdir(destDir, { recursive: true });
  }

  let success = 0;
  for (const pack of itemPacks) {
    try {
      await packItemCompendium(pack);
      success++;
    } catch (error) {
      console.error(`[ERROR] ${pack}: ${error.message}`);
    }
  }

  console.log('\n============================================================');
  console.log(`Compilación completada: ${success}/${itemPacks.length} packs`);
  console.log('============================================================');
  
  if (success === itemPacks.length) {
    console.log('\nPróximos pasos:');
    console.log('1. git add packs/');
    console.log('2. git commit -m "Fix: Compile packs with classic-level"');
    console.log('3. git push');
    console.log('4. Reinstala el módulo en Foundry');
  }
}

/**
 * Compila un pack de items desde archivos JSON
 * @param {string} pack Nombre del pack
 */
async function packItemCompendium(pack) {
  console.log(`\n[${pack}] Compilando...`);
  
  const packPath = path.join(srcDir, pack);
  const dbPath = path.join(destDir, pack);
  
  // Verificar que existe el directorio fuente
  if (!existsSync(packPath)) {
    throw new Error(`Directorio fuente no encontrado: ${packPath}`);
  }
  
  // Limpiar directorio de destino si existe
  if (existsSync(dbPath)) {
    await fs.rm(dbPath, { recursive: true });
  }
  
  // Crear la base de datos LevelDB
  const db = new ClassicLevel(dbPath, {
    keyEncoding: 'utf8',
    valueEncoding: 'json',
  });
  await db.open();
  
  // Crear un batch para insertar todos los documentos
  const batch = db.batch();
  
  // Leer todos los archivos JSON del directorio fuente
  const files = await fs.readdir(packPath);
  const jsonFiles = files.filter(f => f.endsWith('.json'));
  
  if (jsonFiles.length === 0) {
    await db.close();
    throw new Error(`No hay archivos JSON en ${packPath}`);
  }
  
  console.log(`  [OK] Encontrados ${jsonFiles.length} archivos JSON`);
  
  // Procesar cada archivo JSON
  for (const file of jsonFiles) {
    const filePath = path.join(packPath, file);
    const content = await fs.readFile(filePath, 'utf-8');
    const doc = JSON.parse(content);
    
    // Asegurar que tiene _id
    if (!doc._id) {
      doc._id = makeID();
      console.log(`  [WARN] ${file} no tenía _id, generado: ${doc._id}`);
    }
    
    // Asegurar que tiene effects array
    doc.effects = doc.effects || [];
    
    // Construir la clave para LevelDB
    // Formato: !items!<id> para items, !actors!<id> para actores, etc.
    const docType = getDocType(doc.type);
    const key = `!${docType}!${doc._id}`;
    
    // Agregar al batch
    batch.put(key, doc);
    console.log(`  [OK] Agregado: ${doc.name} (${doc._id})`);
  }
  
  // Escribir el batch y cerrar la base de datos
  await batch.write();
  await db.close();
  
  // Verificar que se crearon archivos
  const createdFiles = await fs.readdir(dbPath);
  const ldbFiles = createdFiles.filter(f => f.endsWith('.ldb') || f.endsWith('.log'));
  
  console.log(`  [OK] Compilado: ${jsonFiles.length} documentos en ${createdFiles.length} archivos`);
  
  // Mostrar tamaño total
  let totalSize = 0;
  for (const file of createdFiles) {
    const stat = await fs.stat(path.join(dbPath, file));
    totalSize += stat.size;
  }
  console.log(`  [OK] Tamaño total: ${totalSize} bytes`);
}

/**
 * Determina el tipo de documento para la clave LevelDB
 * @param {string} type Tipo del documento (edge, hindrance, etc.)
 * @returns {string} Tipo para la clave (items, actors, etc.)
 */
function getDocType(type) {
  // Items: edge, hindrance, power, skill, weapon, armor, gear, etc.
  const itemTypes = ['edge', 'hindrance', 'power', 'skill', 'weapon', 'armor', 'gear', 'shield', 'consumable', 'ability'];
  
  // Actors: character, npc, vehicle
  const actorTypes = ['character', 'npc', 'vehicle'];
  
  if (itemTypes.includes(type)) return 'items';
  if (actorTypes.includes(type)) return 'actors';
  if (type === 'journal' || type === 'journalentry') return 'journal';
  
  // Por defecto, items
  return 'items';
}

/**
 * Genera un ID aleatorio de 16 caracteres (formato Foundry)
 * @param {number} length Longitud del ID
 * @returns {string} ID generado
 */
function makeID(length = 16) {
  let result = '';
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// Ejecutar
main().catch(console.error);
