import lotus.domino.*;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.io.BufferedWriter;
import java.util.List;
import java.util.Iterator;

public class JavaAgent extends AgentBase {
    public void NotesMain() {
        // Array de nombres de formularios a exportar
        String[] formNames = {"frmRegistro", "frmProcedimiento", "frmInformacion"}; // Agrega los nombres de tus formularios aquí
        String exportDir = "C:\\Users\\robin\\Desktop\\Centrosur\\RespaldoDomino\\ProPru";

        // Itera sobre cada formulario y llama a exportDocuments
        for (int i = 0; i < formNames.length; i++) {
            String formName = formNames[i];
            System.out.println("Iniciando exportación para el formulario: " + formName);
            exportDocuments(formName, exportDir);
        }
    }

    /**
     * Exporta documentos de la base de datos con el formulario especificado a un directorio CSV.
     *
     * @param formName Nombre del formulario cuyos documentos serán exportados.
     * @param exportDir Directorio donde se guardarán los archivos exportados.
     */
    private void exportDocuments(String formName, String exportDir) {
        Session session = null;
        Database db = null;
        DocumentCollection docs = null;
        Document doc = null;
        Item item = null;
        RichTextItem rtItem = null;
        BufferedWriter writer = null;

        try {
            // Obtiene la sesión actual y la base de datos
            session = getSession();
            db = session.getCurrentDatabase();

            // Define la ruta del directorio donde se guardarán los datos del formulario
            String directoryPath = exportDir + "\\" + formName;

            // Verifica si el directorio existe, si no, lo crea
            File generalDirectory = new File(directoryPath);
            if (!generalDirectory.exists()) {
                boolean success = generalDirectory.mkdirs();
                if (!success) {
                    System.out.println("No se pudo crear la carpeta: " + directoryPath);
                }
            } else {
                System.out.println("La carpeta ya existe: " + directoryPath);
            }

            // Define la ruta para el archivo CSV
            String csvFilePath = directoryPath + "\\documents_info.csv";

            // Muestra mensaje de búsqueda y realiza la búsqueda de documentos
            System.out.println("Buscando documentos con el formulario: " + formName);
            docs = db.search("Form = \"" + formName + "\"");
            System.out.println("Número de documentos encontrados: " + docs.getCount());

            // Crea el archivo CSV con codificación UTF-8
            FileOutputStream fileOutputStream = new FileOutputStream(csvFilePath);
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(fileOutputStream, "UTF-8");
            writer = new BufferedWriter(outputStreamWriter);
            writer.write("DocID,FieldName,FieldValue\n");

            // Procesa cada documento encontrado
            doc = docs.getFirstDocument();
            while (doc != null) {
                String docID = doc.getUniversalID(); // Obtiene el ID universal del documento
                String docDir = directoryPath + "\\" + docID; // Define el directorio para el documento
                File dir = new File(docDir);
                System.out.println("\n-----------------");
                System.out.println("Procesando documento ID: " + docID);
                System.out.println("Creando carpeta para el documento en: " + docDir);

                // Crea el directorio para el documento si no existe
                if (!dir.exists()) {
                    boolean success = dir.mkdirs();
                    if (!success) {
                        System.out.println("No se pudo crear la carpeta: " + docDir);
                    }
                } else {
                    System.out.println("La carpeta ya existe: " + docDir);
                }

                // Exporta los campos del documento y guarda los archivos adjuntos
                List items = doc.getItems();
                System.out.println("Número de items en el documento: " + items.size());
                for (int i = 0; i < items.size(); i++) {
                    item = (Item) items.get(i);
                    String fieldName = item.getName(); // Obtiene el nombre del campo
                    String fieldValue = item.getText(); // Obtiene el valor del campo

                    // Guarda los campos que no son RichText
                    if (!(item instanceof RichTextItem)) {
                        //System.out.println("Guardando campo: " + fieldName);
                        writer.write(docID + "," + fieldName + "," + escapeCsv(fieldValue) + "\n");
                    } else {
                        rtItem = (RichTextItem) item; // Cast para RichTextItem
                        //System.out.println("Procesando RichTextItem: " + fieldName);

                        // Extrae y guarda los archivos adjuntos
                        List embeddedObjects = rtItem.getEmbeddedObjects();
                        Iterator it = embeddedObjects.iterator();
                        while (it.hasNext()) {
                            EmbeddedObject eo = (EmbeddedObject) it.next();
                            try {
                                if (eo != null && eo.getSource() != null) {
                                    String attachmentName = eo.getSource();
                                    File attachmentFile = new File(docDir + "\\" + attachmentName);

                                    //System.out.println("Extrayendo y guardando archivo adjunto: " + attachmentName);
                                    // Guarda el archivo adjunto
                                    InputStream is = eo.getInputStream();
                                    FileOutputStream fos = new FileOutputStream(attachmentFile);
                                    try {
                                        byte[] buffer = new byte[1024];
                                        int length;
                                        while ((length = is.read(buffer)) > 0) {
                                            fos.write(buffer, 0, length);
                                        }
                                        //System.out.println("Archivo adjunto guardado exitosamente: " + attachmentFile.getAbsolutePath());
                                        writer.write(docID + "," + fieldName + "," + attachmentFile.getAbsolutePath() + "\n");
                                    } finally {
                                        fos.close(); // Cierra el FileOutputStream
                                        is.close();  // Cierra el InputStream
                                    }
                                } else {
                                    System.out.println("Objeto embebido sin fuente: " + eo);
                                }
                            } catch (Exception e) {
                                System.out.println("Excepción al procesar EmbeddedObject: " + e.getMessage());
                                e.printStackTrace();
                            }
                        }
                    }
                }

                // Recicla el documento actual y obtiene el siguiente
                Document nextDoc = docs.getNextDocument(doc);
                doc.recycle(); // Libera los recursos del documento actual
                doc = nextDoc; // Pasa al siguiente documento
            }

        } catch (Exception e) {
            // Manejo de excepciones generales
            System.out.println("Error en el agente: " + e.getMessage());
            e.printStackTrace();
        } finally {
            try {
                // Cierra BufferedWriter
                if (writer != null) {
                    System.out.println("Cerrando BufferedWriter...");
                    writer.close();
                }
                // Libera los recursos de DocumentCollection
                if (docs != null) {
                    System.out.println("Reciclaje de DocumentCollection...");
                    docs.recycle();
                }
                // Libera los recursos de Database
                if (db != null) {
                    System.out.println("Reciclaje de Database...");
                    db.recycle();
                }
                // Libera los recursos de Session
                if (session != null) {
                    System.out.println("Reciclaje de Session...");
                    session.recycle();
                }
            } catch (Exception e) {
                // Manejo de excepciones en el bloque finally
                System.out.println("Error al cerrar recursos en finally: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }

    /**
     * Método para escapar caracteres especiales en CSV y eliminar saltos de línea.
     *
     * @param value Valor del campo que se va a escapar.
     * @return Valor escapado en formato CSV.
     */
    private String escapeCsv(String value) {
        if (value == null) {
            return "";
        }
        // Reemplaza saltos de línea y retornos de carro por un espacio
        value = value.replace("\n", " ").replace("\r", " ");
        // Escapa las comillas dobles
        return "\"" + value.replace("\"", "\"\"") + "\"";
    }
}
