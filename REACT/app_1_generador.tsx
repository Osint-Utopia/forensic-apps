import { useState } from 'react';

interface FileNode {
  id: string;
  name: string;
  type: 'folder' | 'file';
  content?: string; // For files
  children?: FileNode[]; // For folders
  isOpen?: boolean; // UI state for folders
}

// Helper to generate unique IDs
const generateId = (): string => Math.random().toString(36).substring(2, 11);

// Recursive component to display a single file/folder item in the tree
interface FileTreeItemProps {
  node: FileNode;
  onDownloadFile: (node: FileNode) => void;
  onToggleFolder: (id: string) => void;
  level: number;
}

const FileTreeItem: React.FC<FileTreeItemProps> = ({ node, onDownloadFile, onToggleFolder, level }) => {
  // Tailwind's spacing scale is based on rem, e.g., pl-4 is 1rem.
  // We want to increment padding by a consistent step, e.g., 1rem for each level.
  // level 0 (root) should have pl-0 or similar, children pl-4, grandchildren pl-8, etc.
  // The list item itself will receive the padding.
  const paddingLeft = level === 0 ? 'pl-0' : `pl-${level * 4}`;

  return (
    <li className={`${paddingLeft} flex flex-col py-1`}>
      <div className="flex items-center justify-between w-full">
        <div className="flex items-center flex-grow">
          {node.type === 'folder' ? (
            <button
              onClick={() => onToggleFolder(node.id)}
              className="flex items-center text-indigo-700 hover:text-indigo-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded px-1 -ml-1 transition duration-150 ease-in-out"
              aria-expanded={node.isOpen}
            >
              <span className="text-xl mr-2">
                {node.isOpen ? '📂' : '📁'}
              </span>
              <span className="font-medium text-gray-800">{node.name}</span>
            </button>
          ) : (
            <span className="flex items-center text-gray-700">
              <span className="text-xl mr-2">📄</span>
              <span className="font-normal text-gray-700">{node.name}</span>
            </span>
          )}
        </div>
        {node.type === 'file' && node.content && (
          <button
            onClick={() => onDownloadFile(node)}
            className="ml-4 px-3 py-1 bg-indigo-500 text-white text-sm rounded-md hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-150 ease-in-out"
          >
            Descargar
          </button>
        )}
      </div>
      {node.type === 'folder' && node.isOpen && node.children && node.children.length > 0 && (
        <ul className="space-y-1 mt-1">
          {node.children.map((childNode) => (
            <FileTreeItem
              key={childNode.id}
              node={childNode}
              onDownloadFile={onDownloadFile}
              onToggleFolder={onToggleFolder}
              level={level + 1}
            />
          ))}
        </ul>
      )}
    </li>
  );
};

// Component to render the full file tree structure
interface FileTreeDisplayProps {
  nodes: FileNode[];
  onDownloadFile: (node: FileNode) => void;
  onToggleFolder: (id: string) => void;
  level?: number;
}

const FileTreeDisplay: React.FC<FileTreeDisplayProps> = ({ nodes, onDownloadFile, onToggleFolder, level = 0 }) => {
  return (
    <ul className="space-y-1">
      {nodes.map((node) => (
        <FileTreeItem
          key={node.id}
          node={node}
          onDownloadFile={onDownloadFile}
          onToggleFolder={onToggleFolder}
          level={level}
        />
      ))}
    </ul>
  );
};

const ProjectGeneratorApp: React.FC = () => {
  const [projectName, setProjectName] = useState<string>('MyAwesomeProject');
  const [filesGenerated, setFilesGenerated] = useState<FileNode[]>([]);
  const [statusMessage, setStatusMessage] = useState<string>('');

  // Function to generate a default React project structure
  const generateInitialStructure = (name: string): FileNode => {
    return {
      id: generateId(),
      name: name,
      type: 'folder',
      isOpen: true, // Root folder is open by default
      children: [
        {
          id: generateId(),
          name: 'public',
          type: 'folder',
          isOpen: false,
          children: [
            {
              id: generateId(),
              name: 'index.html',
              type: 'file',
              content: `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${name}</title>
  <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
</body>
</html>`,
            },
            {
              id: generateId(),
              name: 'favicon.ico',
              type: 'file',
              content: `This is a placeholder for favicon.ico.`,
            },
          ],
        },
        {
          id: generateId(),
          name: 'src',
          type: 'folder',
          isOpen: true,
          children: [
            {
              id: generateId(),
              name: 'App.tsx',
              type: 'file',
              content: `import React from 'react';\n\nconst App: React.FC = () => {\n  return (\n    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">\n      <h1 className="text-5xl font-extrabold text-indigo-700 text-center">\n        ¡Hola, ${name}!\n      </h1>\n    </div>\n  );\n};\n\nexport default App;\n`,
            },
            {
              id: generateId(),
              name: 'index.tsx',
              type: 'file',
              content: `import React from 'react';\nimport ReactDOM from 'react-dom/client';\nimport App from './App';\nimport './index.css';\n\nconst root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);\nroot.render(\n  <React.StrictMode>\n    <App />\n  </React.StrictMode>\n);\n`,
            },
            {
              id: generateId(),
              name: 'index.css',
              type: 'file',
              content: `@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\n/* Custom styles can go here */\n`,
            },
            {
              id: generateId(),
              name: 'reportWebVitals.ts',
              type: 'file',
              content: `import { ReportHandler } from 'web-vitals';\n\nconst reportWebVitals = (onPerfEntry?: ReportHandler) => {\n  if (onPerfEntry && onPerfEntry instanceof Function) {\n    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {\n      getCLS(onPerfEntry);\n      getFID(onPerfEntry);\n      getFCP(onPerfEntry);\n      getLCP(onPerfEntry);\n      getTTFB(onPerfEntry);\n    });\n  }\n};\n\nexport default reportWebVitals;\n`,
            },
            {
              id: generateId(),
              name: 'components',
              type: 'folder',
              isOpen: false,
              children: [
                {
                  id: generateId(),
                  name: 'Button.tsx',
                  type: 'file',
                  content: `import React from 'react';\n\ninterface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {\n  children: React.ReactNode;\n}\n\nconst Button: React.FC<ButtonProps> = ({ children, className, ...props }) => {\n  return (\n    <button\n      className={\`px-5 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200 ease-in-out \${className || ''}\`}\n      {...props}\n    >\n      {children}\n    </button>\n  );\n};\n\nexport default Button;\n`,
                },
              ],
            },
          ],
        },
        {
          id: generateId(),
          name: 'package.json',
          type: 'file',
          content: `{
  "name": "${name.toLowerCase().replace(/\s/g, '-')}",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "web-vitals": "^2.1.4"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^4.9.5",
    "tailwindcss": "^3.3.3",
    "postcss": "^8.4.29",
    "autoprefixer": "^10.4.16",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}`,
        },
        {
          id: generateId(),
          name: '.gitignore',
          type: 'file',
          content: `node_modules\n.env\nbuild\n*.log\n`,
        },
        {
          id: generateId(),
          name: 'README.md',
          type: 'file',
          content: `# ${name}\n\nEste es un proyecto React generado automáticamente con una estructura básica.\n\n## Scripts Disponibles\n\nEn el directorio del proyecto, puedes ejecutar:\n\n### \`npm start\`\n\nEjecuta la aplicación en modo desarrollo.\nAbre [http://localhost:3000](http://localhost:3000) para verla en el navegador.\n\nLa página se recargará si haces modificaciones.\nTambién verás cualquier error de lint en la consola.\n\n### \`npm test\`\n\nLanza el ejecutor de pruebas en el modo de vigilancia interactiva.\nConsulta la sección sobre [ejecución de pruebas](https://facebook.github.io/create-react-app/docs/running-tests) para más información.\n\n### \`npm run build\`\n\nConstruye la aplicación para producción en la carpeta \`build\`.\nEmpaqueta React en modo de producción y optimiza la compilación para el mejor rendimiento.\n\nLa compilación se minifica y los nombres de archivo incluyen los hashes.\n¡Tu aplicación está lista para ser desplegada!\n\nConsulta la sección sobre [despliegue](https://facebook.github.io/create-react-app/docs/deployment) para más información.\n`,
        },
        {
          id: generateId(),
          name: 'tailwind.config.js',
          type: 'file',
          content: `/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}`,
        },
        {
          id: generateId(),
          name: 'tsconfig.json',
          type: 'file',
          content: `{
  "compilerOptions": {
    "target": "es5",
    "lib": [
      "dom",
      "dom.iterable",
      "esnext"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": [
    "src"
  ]
}`,
        },
      ],
    };
  };

  const handleGenerateProject = () => {
    if (!projectName.trim()) {
      setStatusMessage('Por favor, ingresa un nombre para el proyecto.');
      return;
    }
    const rootNode = generateInitialStructure(projectName.trim());
    setFilesGenerated([rootNode]);
    setStatusMessage(`¡Estructura de proyecto "${projectName}" generada virtualmente! Explora y descarga tus archivos.`);
  };

  const handleDownloadFile = (node: FileNode) => {
    if (node.type === 'file' && node.content) {
      const blob = new Blob([node.content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = node.name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      setStatusMessage(`Archivo "${node.name}" descargado exitosamente.`);
    } else {
      setStatusMessage(`No se puede descargar "${node.name}". No es un archivo o no tiene contenido.`);
    }
  };

  // Function to recursively update folder open state
  const toggleFolder = (nodes: FileNode[], idToToggle: string): FileNode[] => {
    return nodes.map((node) => {
      if (node.id === idToToggle && node.type === 'folder') {
        return { ...node, isOpen: !node.isOpen };
      }
      if (node.type === 'folder' && node.children) {
        return { ...node, children: toggleFolder(node.children, idToToggle) };
      }
      return node;
    });
  };

  const handleToggleFolder = (id: string) => {
    setFilesGenerated((prevNodes) => toggleFolder(prevNodes, id));
  };


  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-800">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-xl p-8 border border-gray-200">
        <h1 className="text-4xl font-extrabold text-indigo-700 mb-6 text-center">
          Generador de Proyectos React
        </h1>
        <p className="text-lg text-gray-600 mb-8 text-center">
          Crea una estructura de proyecto React virtual en tu navegador. Puedes expandir/colapsar carpetas
          y descargar archivos individuales para usarlos en tu proyecto local.
          <br />
          <span className="font-medium text-red-600">
            (Nota Importante: Los navegadores, por seguridad, no permiten la creación directa de carpetas en tu sistema de archivos local,
            pero puedes descargar todos los archivos generados individualmente.)
          </span>
        </p>

        <div className="mb-8 p-6 bg-indigo-50 rounded-lg border border-indigo-200">
          <label htmlFor="projectName" className="block text-lg font-semibold text-indigo-800 mb-2">
            Nombre del Proyecto:
          </label>
          <input
            type="text"
            id="projectName"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-lg text-gray-800 transition duration-150 ease-in-out"
            placeholder="Ej: MiAplicacionFantastica"
          />
          <button
            onClick={handleGenerateProject}
            className="mt-6 w-full py-3 bg-indigo-600 text-white font-bold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-150 ease-in-out text-lg"
          >
            Generar Estructura del Proyecto
          </button>
        </div>

        {statusMessage && (
          <div className="mb-8 p-4 bg-indigo-100 border border-indigo-300 text-indigo-800 rounded-md font-medium text-center">
            {statusMessage}
          </div>
        )}

        {filesGenerated.length > 0 && (
          <div className="bg-gray-100 p-6 rounded-lg border border-gray-200">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Estructura Generada:
            </h2>
            <div className="text-sm text-gray-600 mb-4">
              Haz clic en los iconos de carpeta para expandirlas/colapsarlas. Usa el botón "Descargar" para guardar un archivo individualmente.
            </div>
            <FileTreeDisplay
              nodes={filesGenerated}
              onDownloadFile={handleDownloadFile}
              onToggleFolder={handleToggleFolder}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectGeneratorApp;