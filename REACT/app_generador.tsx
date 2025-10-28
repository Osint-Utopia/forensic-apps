import { useState, Fragment } from 'react';

// 1. Type Definitions
interface FileSystemItem {
    name: string;
    type: 'file' | 'folder';
    children?: FileSystemItem[];
    isOpen?: boolean; // Only for folders, to toggle visibility of children
}

// 2. Initial Data for forensic-lab structure
// This constant defines the default file and folder structure.
const initialForensicLabStructure: FileSystemItem[] = [
    {
        name: 'forensic-lab',
        type: 'folder',
        isOpen: true, // Root folder starts open for immediate visibility
        children: [
            {
                name: 'assets',
                type: 'folder',
                isOpen: false,
                children: [
                    {
                        name: 'css',
                        type: 'folder',
                        isOpen: false,
                        children: [
                            { name: 'main.css', type: 'file' },
                            { name: 'components.css', type: 'file' },
                            { name: 'themes.css', type: 'file' },
                        ],
                    },
                    {
                        name: 'js',
                        type: 'folder',
                        isOpen: false,
                        children: [
                            {
                                name: 'core',
                                type: 'folder',
                                isOpen: false,
                                children: [
                                    { name: 'app.js', type: 'file' },
                                    { name: 'embeddings.js', type: 'file' },
                                    { name: 'local-ai.js', type: 'file' },
                                    { name: 'storage.js', type: 'file' },
                                ],
                            },
                            {
                                name: 'modules',
                                type: 'folder',
                                isOpen: false,
                                children: [
                                    { name: 'document-analyzer.js', type: 'file' },
                                    { name: 'evidence-processor.js', type: 'file' },
                                    { name: 'report-generator.js', type: 'file' },
                                    { name: 'case-manager.js', type: 'file' },
                                ],
                            },
                            {
                                name: 'utils',
                                type: 'folder',
                                isOpen: false,
                                children: [
                                    { name: 'file-handler.js', type: 'file' },
                                    { name: 'format-utils.js', type: 'file' },
                                    { name: 'validation.js', type: 'file' },
                                ],
                            },
                        ],
                    },
                    {
                        name: 'images',
                        type: 'folder',
                        isOpen: false,
                        children: [
                            { name: 'icons', type: 'folder', isOpen: false, children: [] },
                            { name: 'backgrounds', type: 'folder', isOpen: false, children: [] },
                        ],
                    },
                ],
            },
            {
                name: 'data',
                type: 'folder',
                isOpen: false,
                children: [
                    {
                        name: 'models',
                        type: 'folder',
                        isOpen: false,
                        children: [
                            {
                                name: 'document-templates',
                                type: 'folder',
                                isOpen: false,
                                children: [
                                    { name: 'informe-criminalistica.json', type: 'file' },
                                    { name: 'dictamen-fotografico.json', type: 'file' },
                                    { name: 'analisis-documentoscopia.json', type: 'file' },
                                    { name: 'reporte-informatica-forense.json', type: 'file' },
                                ],
                            },
                            {
                                name: 'embeddings',
                                type: 'folder',
                                isOpen: false,
                                children: [
                                    { name: 'forensic-knowledge.json', type: 'file' },
                                    { name: 'user-templates.json', type: 'file' },
                                ],
                            },
                            {
                                name: 'prompts',
                                type: 'folder',
                                isOpen: false,
                                children: [
                                    { name: 'forensic-prompts.json', type: 'file' },
                                    { name: 'custom-prompts.json', type: 'file' },
                                ],
                            },
                        ],
                    },
                    {
                        name: 'knowledge-base',
                        type: 'folder',
                        isOpen: false,
                        children: [
                            { name: 'procedures', type: 'folder', isOpen: false, children: [] },
                            { name: 'regulations', type: 'folder', isOpen: false, children: [] },
                            { name: 'case-studies', type: 'folder', isOpen: false, children: [] },
                        ],
                    },
                    {
                        name: 'user-data',
                        type: 'folder',
                        isOpen: false,
                        children: [
                            { name: 'cases', type: 'folder', isOpen: false, children: [] },
                            { name: 'reports', type: 'folder', isOpen: false, children: [] },
                            { name: 'templates', type: 'folder', isOpen: false, children: [] },
                        ],
                    },
                ],
            },
            {
                name: 'libs',
                type: 'folder',
                isOpen: false,
                children: [
                    {
                        name: 'ai-models',
                        type: 'folder',
                        isOpen: false,
                        children: [
                            { name: 'llama-integration.js', type: 'file' },
                            { name: 'mistral-integration.js', type: 'file' },
                            { name: 'local-embeddings.js', type: 'file' },
                        ],
                    },
                    {
                        name: 'external',
                        type: 'folder',
                        isOpen: false,
                        children: [
                            { name: 'pdf-lib.min.js', type: 'file' },
                            { name: 'docx-generator.min.js', type: 'file' },
                            { name: 'exif-reader.min.js', type: 'file' },
                        ],
                    },
                    {
                        name: 'workers',
                        type: 'folder',
                        isOpen: false,
                        children: [
                            { name: 'ai-worker.js', type: 'file' },
                            { name: 'embedding-worker.js', type: 'file' },
                        ],
                    },
                ],
            },
            {
                name: 'components',
                type: 'folder',
                isOpen: false,
                children: [
                    { name: 'header.html', type: 'file' },
                    { name: 'sidebar.html', type: 'file' },
                    { name: 'evidence-uploader.html', type: 'file' },
                    { name: 'chat-interface.html', type: 'file' },
                    { name: 'report-viewer.html', type: 'file' },
                ],
            },
            {
                name: 'config',
                type: 'folder',
                isOpen: false,
                children: [
                    { name: 'app-config.json', type: 'file' },
                    { name: 'model-config.json', type: 'file' },
                    { name: 'user-settings.json', type: 'file' },
                ],
            },
            { name: 'index.html', type: 'file' },
            { name: 'manifest.json (PWA)', type: 'file' },
            { name: 'service-worker.js', type: 'file' },
            { name: 'README.md', type: 'file' },
        ],
    },
];

// Helper Component for rendering a single file/folder item in the tree view
interface FileStructureItemProps {
    item: FileSystemItem;
    depth: number;
    itemPath: string; // e.g., "0.children[1].children[0]" used for unique identification and state updates
    onToggle: (path: string) => void;
    onAddItem: (parentPath: string, newItem: FileSystemItem) => void;
}

const FileStructureItem: React.FC<FileStructureItemProps> = ({ item, depth, itemPath, onToggle, onAddItem }) => {
    const [isAdding, setIsAdding] = useState<boolean>(false);
    const [newItemName, setNewItemName] = useState<string>('');
    const [newItemType, setNewItemType] = useState<'file' | 'folder'>('file');

    // Toggles the 'isOpen' state for folders
    const handleToggleClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        if (item.type === 'folder') {
            onToggle(itemPath);
        }
    };

    // Initiates the process of adding a new item (shows input fields)
    const handleAddItemClick = (e: React.MouseEvent) => {
        e.stopPropagation(); // Prevent parent folder toggle from firing
        if (item.type === 'folder') {
            setIsAdding(true);
            setNewItemName('');
            setNewItemType('file'); // Default to file
        }
    };

    // Saves the newly added item to the structure
    const handleSaveNewItem = (e: React.MouseEvent) => {
        e.stopPropagation();
        if (newItemName.trim() && item.type === 'folder') {
            const newItem: FileSystemItem = {
                name: newItemName.trim(),
                type: newItemType,
                children: newItemType === 'folder' ? [] : undefined,
                isOpen: newItemType === 'folder' ? true : undefined, // New folders start open
            };
            onAddItem(itemPath, newItem);
            setIsAdding(false);
            setNewItemName('');
        }
    };

    // Cancels the add item operation
    const handleCancelAddItem = (e: React.MouseEvent) => {
        e.stopPropagation();
        setIsAdding(false);
        setNewItemName('');
    };

    // Tailwind class for dynamic indentation based on depth
    const indentClass = `pl-${depth * 6}`;

    return (
        <div className="flex flex-col">
            <div className={`flex items-center py-1.5 ${indentClass}`}>
                {item.type === 'folder' ? (
                    <button
                        onClick={handleToggleClick}
                        className="flex items-center text-blue-700 hover:text-blue-900 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-300 rounded-sm group"
                    >
                        <span className="w-4 h-4 flex items-center justify-center text-blue-500 mr-1 text-base">
                            {item.isOpen ? '▼' : '▶'}
                        </span>
                        <span className="font-medium text-gray-800">{item.name}</span>
                        <button
                            onClick={handleAddItemClick}
                            className="ml-2 text-gray-500 hover:text-gray-700 opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-300 text-sm leading-none"
                            aria-label="Add item"
                            title="Add new file or folder"
                        >
                            +
                        </button>
                    </button>
                ) : (
                    <div className="flex items-center">
                        <span className="w-4 h-4 flex items-center justify-center text-gray-500 mr-1 text-base">📄</span>
                        <span className="text-gray-700">{item.name}</span>
                    </div>
                )}
            </div>

            {isAdding && item.type === 'folder' && (
                <div className={`flex items-center my-2 ${indentClass} pl-6 border-l-2 border-blue-100`}>
                    <input
                        type="text"
                        value={newItemName}
                        onChange={(e) => setNewItemName(e.target.value)}
                        placeholder="New item name"
                        className="p-2 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-200 w-48 shadow-sm"
                    />
                    <select
                        value={newItemType}
                        onChange={(e) => setNewItemType(e.target.value as 'file' | 'folder')}
                        className="ml-2 p-2 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-200 shadow-sm bg-white"
                    >
                        <option value="file">File</option>
                        <option value="folder">Folder</option>
                    </select>
                    <button
                        onClick={handleSaveNewItem}
                        className="ml-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-300 shadow-sm"
                    >
                        Save
                    </button>
                    <button
                        onClick={handleCancelAddItem}
                        className="ml-2 px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 transition-colors text-sm font-medium focus:outline-none focus:ring-2 focus:ring-gray-300 shadow-sm"
                    >
                        Cancel
                    </button>
                </div>
            )}

            {item.isOpen && item.children && item.children.length > 0 && (
                <div className="border-l-2 border-blue-100 ml-3"> {/* Visual line connecting children */}
                    {item.children.map((child, index) => (
                        <FileStructureItem
                            key={`${itemPath}.children[${index}]`} // Stable and unique key
                            item={child}
                            depth={depth + 1}
                            itemPath={`${itemPath}.children[${index}]`}
                            onToggle={onToggle}
                            onAddItem={onAddItem}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

// Main React component for the File Structure Generator
const FileStructureGenerator: React.FC = () => {
    const [structure, setStructure] = useState<FileSystemItem[]>(initialForensicLabStructure);

    // Utility function to immutably update a nested item within the tree state
    const updateTree = (
        rootItems: FileSystemItem[],
        targetPath: string, // e.g., "0.children[1].children[0]"
        updater: (item: FileSystemItem) => FileSystemItem
    ): FileSystemItem[] => {
        const pathSegments = targetPath.split('.');

        const recursiveUpdate = (
            currentNodes: FileSystemItem[],
            segmentIndex: number
        ): FileSystemItem[] => {
            if (segmentIndex >= pathSegments.length) {
                // This condition should ideally not be reached if the path is valid and points to an existing item
                return currentNodes;
            }

            const segment = pathSegments[segmentIndex];
            let indexInArray: number | null = null;

            // Parse the segment to determine if it's a direct index (for root items) or a 'children[index]' format
            const rootIndexMatch = segment.match(/^(\d+)$/);
            const childrenIndexMatch = segment.match(/^children\[(\d+)\]$/);

            if (rootIndexMatch) {
                indexInArray = parseInt(rootIndexMatch[1], 10);
            } else if (childrenIndexMatch) {
                indexInArray = parseInt(childrenIndexMatch[1], 10);
            } else {
                console.error("Invalid path segment format:", segment);
                return currentNodes; // Return original if segment is malformed
            }

            // Validate the parsed index
            if (indexInArray === null || isNaN(indexInArray) || indexInArray < 0 || indexInArray >= currentNodes.length) {
                console.error("Index out of bounds or invalid for segment:", segment, currentNodes);
                return currentNodes; // Return original if index is invalid
            }

            // Create a shallow copy of the current array to ensure immutability
            const newNodes = [...currentNodes];
            const nodeToProcess = newNodes[indexInArray];

            if (segmentIndex === pathSegments.length - 1) {
                // This is the target node: apply the updater function
                newNodes[indexInArray] = updater(nodeToProcess);
            } else {
                // Not the target yet, continue traversing deeper
                if (nodeToProcess.type === 'folder' && nodeToProcess.children) {
                    // Recurse into children, creating new objects up the chain
                    newNodes[indexInArray] = {
                        ...nodeToProcess,
                        children: recursiveUpdate(nodeToProcess.children, segmentIndex + 1),
                    };
                } else {
                    console.warn("Attempted to traverse into a non-folder or non-existent children path:", targetPath, segmentIndex);
                }
            }
            return newNodes;
        };

        return recursiveUpdate(rootItems, 0);
    };

    // Handler to toggle the 'isOpen' state of a folder
    const handleToggle = (path: string) => {
        setStructure(prevStructure => updateTree(prevStructure, path, item => ({ ...item, isOpen: !item.isOpen })));
    };

    // Handler to add a new FileSystemItem to a parent folder
    const handleAddItem = (parentPath: string, newItem: FileSystemItem) => {
        setStructure(prevStructure =>
            updateTree(prevStructure, parentPath, item => {
                if (item.type === 'folder') {
                    // If the item is a folder, add the new item to its children
                    return {
                        ...item,
                        children: item.children ? [...item.children, newItem] : [newItem],
                        isOpen: true, // Automatically open the parent folder when a new item is added
                    };
                }
                return item; // Return item unchanged if not a folder (shouldn't happen with UI logic)
            })
        );
    };

    // Resets the structure to its predefined initial state
    const handleResetStructure = () => {
        setStructure(initialForensicLabStructure);
    };

    // Allows adding a new item directly to the root level of the structure
    const handleAddRootItem = () => {
        const newItemName = prompt("Enter name for new root item:");
        if (newItemName) {
            const newItemType = confirm("Is this a folder? (OK for folder, Cancel for file)") ? 'folder' : 'file';
            const newItem: FileSystemItem = {
                name: newItemName.trim(),
                type: newItemType,
                children: newItemType === 'folder' ? [] : undefined,
                isOpen: newItemType === 'folder' ? true : undefined,
            };
            setStructure(prevStructure => [...prevStructure, newItem]);
        }
    };

    return (
        <div className="p-8 bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen text-gray-900 font-sans">
            <div className="max-w-4xl mx-auto bg-white p-6 rounded-xl shadow-lg border border-blue-100">
                <h1 className="text-3xl font-bold text-blue-800 mb-6 border-b pb-3 border-blue-200">
                    Forensic Lab File Structure Generator
                </h1>

                <div className="flex flex-wrap gap-4 mb-6">
                    <button
                        onClick={handleResetStructure}
                        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-300 font-medium shadow-md flex-grow sm:flex-grow-0"
                    >
                        Reset to Default Structure
                    </button>
                    <button
                        onClick={handleAddRootItem}
                        className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-300 font-medium shadow-md flex-grow sm:flex-grow-0"
                    >
                        Add New Root Item
                    </button>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 text-gray-800">
                    <h2 className="text-xl font-semibold mb-4 text-blue-700">Current Structure:</h2>
                    {structure.length === 0 ? (
                        <p className="text-gray-600 italic p-2">
                            No items in the structure. Use "Add New Root Item" to begin!
                        </p>
                    ) : (
                        <div className="flex flex-col">
                            {structure.map((item, index) => (
                                <FileStructureItem
                                    key={`${index}`} // Root items use their index as the path segment
                                    item={item}
                                    depth={0} // Root items are at depth 0
                                    itemPath={`${index}`} // Path for root items is just their index
                                    onToggle={handleToggle}
                                    onAddItem={handleAddItem}
                                />
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default FileStructureGenerator;