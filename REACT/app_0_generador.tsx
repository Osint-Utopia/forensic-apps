import { useState, useEffect } from 'react';

// --- Type Definitions ---
interface FileNode {
  id: string;
  name: string;
  type: 'file';
  extension: string;
}

interface FolderNode {
  id: string;
  name: string;
  type: 'folder';
  children: Array<FileNode | FolderNode>;
}

type StructureNode = FileNode | FolderNode;

type NewItemType = 'folder' | 'file';

// --- Helper Functions ---
function generateUniqueId(): string {
  return Math.random().toString(36).substring(2, 9);
}

// Helper to find a folder by path and optionally create intermediate ones
function findOrCreateFolder(
  root: FolderNode,
  pathSegments: string[],
): { targetFolder: FolderNode | null; error?: string } {
  let current: FolderNode = root;
  const pathExists: string[] = [root.name];

  for (let i = 0; i < pathSegments.length; i++) {
    const segment = pathSegments[i];
    if (!segment) continue; // Skip empty segments

    let foundChild = current.children.find(
      (child) => child.type === 'folder' && child.name === segment
    ) as FolderNode | undefined;

    if (!foundChild) {
      const newFolder: FolderNode = {
        id: generateUniqueId(),
        name: segment,
        type: 'folder',
        children: [],
      };
      current.children.push(newFolder);
      current = newFolder;
    } else {
      current = foundChild;
    }
    pathExists.push(segment);
  }
  return { targetFolder: current };
}

// Helper to build the tree string for download
function buildTreeString(node: StructureNode, indent: string = '', isLast: boolean = false, isRoot: boolean = true): string {
  let tree = '';
  const currentIndent = isRoot ? '' : indent + (isLast ? '└── ' : '├── ');

  if (node.type === 'folder') {
    tree += `${currentIndent}${node.name}/\n`;
    if (node.children && node.children.length > 0) {
      const childrenIndent = isRoot ? indent : indent + (isLast ? '    ' : '│   ');
      node.children.forEach((child, index) => {
        const childIsLast = index === node.children!.length - 1;
        tree += buildTreeString(child, childrenIndent, childIsLast, false);
      });
    }
  } else {
    tree += `${currentIndent}${node.name}.${node.extension}\n`;
  }
  return tree;
}

// --- React Component ---
const FolderStructureApp: React.FC = () => {
  const [rootName, setRootName] = useState<string>('my-project');
  const [rootStructure, setRootStructure] = useState<FolderNode>({
    id: generateUniqueId(),
    name: 'my-project',
    type: 'folder',
    children: [],
  });

  const [parentPathInput, setParentPathInput] = useState<string>('');
  const [newItemNameInput, setNewItemNameInput] = useState<string>('');
  const [newItemTypeInput, setNewItemTypeInput] = useState<NewItemType>('folder');
  const [fileExtensionInput, setFileExtensionInput] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Update root structure name when rootName changes
  useEffect(() => {
    setRootStructure((prev) => ({ ...prev, name: rootName }));
  }, [rootName]);

  const handleAddItem = () => {
    setErrorMessage(null); // Clear previous errors

    if (!newItemNameInput.trim()) {
      setErrorMessage('El nombre del nuevo elemento no puede estar vacío.');
      return;
    }

    if (newItemTypeInput === 'file' && !fileExtensionInput.trim()) {
      setErrorMessage('La extensión del archivo no puede estar vacía para un archivo.');
      return;
    }

    const pathSegments = parentPathInput
      .split('/')
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    // Deep copy of the root structure to ensure immutability
    const newRootStructure = JSON.parse(JSON.stringify(rootStructure)) as FolderNode;

    const { targetFolder, error } = findOrCreateFolder(newRootStructure, pathSegments);

    if (error) {
      setErrorMessage(error);
      return;
    }

    if (!targetFolder) {
      setErrorMessage('Error interno: No se pudo encontrar o crear la carpeta destino.');
      return;
    }

    // Check for duplicate name in the target folder
    const isDuplicate = targetFolder.children.some((item) => {
      const nameMatch = item.name === newItemNameInput.trim();
      if (item.type === 'file' && newItemTypeInput === 'file') {
        return nameMatch && (item as FileNode).extension === fileExtensionInput.trim();
      }
      return nameMatch && item.type === newItemTypeInput;
    });

    if (isDuplicate) {
      setErrorMessage(`Ya existe un ${newItemTypeInput} llamado "${newItemNameInput}" en esta ruta.`);
      return;
    }

    // Create the new item
    let newItem: StructureNode;
    if (newItemTypeInput === 'folder') {
      newItem = {
        id: generateUniqueId(),
        name: newItemNameInput.trim(),
        type: 'folder',
        children: [],
      };
    } else {
      newItem = {
        id: generateUniqueId(),
        name: newItemNameInput.trim(),
        type: 'file',
        extension: fileExtensionInput.trim(),
      };
    }

    targetFolder.children.push(newItem);
    // Sort children for consistent display
    targetFolder.children.sort((a, b) => {
      if (a.type === 'folder' && b.type === 'file') return -1;
      if (a.type === 'file' && b.type === 'folder') return 1;
      return a.name.localeCompare(b.name);
    });

    setRootStructure(newRootStructure);

    // Clear input fields
    setNewItemNameInput('');
    setFileExtensionInput('');
    setParentPathInput('');
  };

  const handleDownload = () => {
    const treeString = buildTreeString(rootStructure);
    const blob = new Blob([treeString], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${rootName}_structure.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Component to render a single node for the preview
  const StructureNodeDisplay: React.FC<{ node: StructureNode; level: number }> = ({ node, level }) => {
    const indent = level * 4; // Using rem or a fixed pixel value can be tricky with Tailwind classes only

    return (
      <div className="flex items-center py-0.5" style={{ paddingLeft: `${indent}rem` }}>
        {node.type === 'folder' ? (
          <span className="text-indigo-700 font-medium mr-1">📁 {node.name}/</span>
        ) : (
          <span className="text-gray-700 text-sm mr-1">📄 {node.name}.{node.extension}</span>
        )}
      </div>
    );
  };

  // Recursive rendering function for the structure preview
  const renderStructure = (node: StructureNode, level: number): JSX.Element => (
    <div key={node.id}>
      <StructureNodeDisplay node={node} level={level} />
      {node.type === 'folder' && node.children && node.children.map((child) => (
        renderStructure(child, level + 1)
      ))}
    </div>
  );

  return (
    <div className="bg-gray-50 min-h-screen p-6 sm:p-8 flex flex-col items-center">
      <div className="bg-white shadow-xl rounded-lg p-6 sm:p-8 w-full max-w-4xl space-y-8">
        <h1 className="text-4xl font-extrabold text-indigo-800 text-center mb-8">Generador de Estructura de Proyecto</h1>

        {/* Root Folder Configuration */}
        <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-5">
          <h2 className="text-2xl font-semibold text-indigo-700 mb-4">Configurar Carpeta Raíz</h2>
          <div className="flex flex-col sm:flex-row items-baseline sm:items-center space-y-3 sm:space-y-0 sm:space-x-4">
            <label htmlFor="root-name" className="text-lg text-gray-700 font-medium whitespace-nowrap">
              Nombre de la carpeta raíz:
            </label>
            <input
              id="root-name"
              type="text"
              value={rootName}
              onChange={(e) => setRootName(e.target.value)}
              className="flex-grow p-2 border border-indigo-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-150 ease-in-out"
              placeholder="Ej: my-project"
            />
          </div>
        </div>

        {/* Add New Item */}
        <div className="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Añadir Nuevo Elemento</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="parent-path" className="block text-sm font-medium text-gray-700 mb-1">
                Ruta padre (relativa a la raíz, ej: assets/images):
              </label>
              <input
                id="parent-path"
                type="text"
                value={parentPathInput}
                onChange={(e) => setParentPathInput(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-150 ease-in-out"
                placeholder="Deja vacío para añadir directamente a la raíz"
              />
            </div>

            <div>
              <label htmlFor="new-item-name" className="block text-sm font-medium text-gray-700 mb-1">
                Nombre del nuevo elemento:
              </label>
              <input
                id="new-item-name"
                type="text"
                value={newItemNameInput}
                onChange={(e) => setNewItemNameInput(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-150 ease-in-out"
                placeholder="Ej: my-component / logo"
              />
            </div>

            <div className="flex flex-col sm:flex-row sm:space-x-4 space-y-4 sm:space-y-0">
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tipo de elemento:
                </label>
                <div className="flex space-x-4">
                  <label className="inline-flex items-center">
                    <input
                      type="radio"
                      className="form-radio text-indigo-600"
                      name="itemType"
                      value="folder"
                      checked={newItemTypeInput === 'folder'}
                      onChange={() => setNewItemTypeInput('folder')}
                    />
                    <span className="ml-2 text-gray-700">Carpeta</span>
                  </label>
                  <label className="inline-flex items-center">
                    <input
                      type="radio"
                      className="form-radio text-indigo-600"
                      name="itemType"
                      value="file"
                      checked={newItemTypeInput === 'file'}
                      onChange={() => setNewItemTypeInput('file')}
                    />
                    <span className="ml-2 text-gray-700">Archivo</span>
                  </label>
                </div>
              </div>

              {newItemTypeInput === 'file' && (
                <div className="flex-1">
                  <label htmlFor="file-extension" className="block text-sm font-medium text-gray-700 mb-1">
                    Extensión del archivo:
                  </label>
                  <input
                    id="file-extension"
                    type="text"
                    value={fileExtensionInput}
                    onChange={(e) => setFileExtensionInput(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-150 ease-in-out"
                    placeholder="Ej: js, tsx, css, html, png"
                  />
                </div>
              )}
            </div>

            {errorMessage && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md relative" role="alert">
                <span className="block sm:inline">{errorMessage}</span>
              </div>
            )}

            <button
              onClick={handleAddItem}
              className="w-full sm:w-auto px-6 py-2 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-150 ease-in-out"
            >
              Añadir Elemento
            </button>
          </div>
        </div>

        {/* Structure Preview */}
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-5 shadow-sm">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Vista Previa de la Estructura</h2>
          <div className="bg-white border border-gray-300 rounded-md p-4 max-h-80 overflow-auto">
            {rootStructure ? renderStructure(rootStructure, 0) : <p className="text-gray-500">La estructura está vacía.</p>}
          </div>
          <button
            onClick={handleDownload}
            className="mt-6 w-full sm:w-auto px-6 py-2 bg-green-600 text-white font-semibold rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition duration-150 ease-in-out"
          >
            Descargar Estructura (.txt)
          </button>
        </div>
      </div>
    </div>
  );
};

export default FolderStructureApp;