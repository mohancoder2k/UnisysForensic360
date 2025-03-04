import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import * as THREE from "three";

// Load the static room model (Always GLB)
function RoomModel({ setFloorHeight }) {
    const { scene } = useGLTF("/scene.glb"); // Room model is a .glb file

    React.useEffect(() => {
        let bbox = new THREE.Box3().setFromObject(scene);
        let minY = bbox.min.y;
        setFloorHeight(minY + 0.01);
    }, [scene, setFloorHeight]);

    return <primitive object={scene} scale={1} />;
}

// Load Uploaded Models (GLB/GLTF)
function UploadedModel({ modelUrl }) {
    const { scene } = useGLTF(modelUrl, true);

    return <primitive object={scene} scale={0.2} position={[0, 0.08, 0]} />;
}

function App() {
    const [floorHeight, setFloorHeight] = useState(0);
    const [uploadedModel, setUploadedModel] = useState(null);

    // Handle GLB/GLTF file upload
    const handleModelUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const fileType = file.name.split('.').pop().toLowerCase();
            if (fileType !== "glb" && fileType !== "gltf") {
                alert("Please upload a .glb or .gltf file");
                return;
            }
            const url = URL.createObjectURL(file);
            setUploadedModel(url);
        }
    };

    return (
        <div style={{ width: "100vw", height: "100vh", position: "relative" }}>
            {/* Upload Button */}
            <input 
                type="file" 
                accept=".glb,.gltf" 
                onChange={handleModelUpload} 
                style={{
                    position: "absolute",
                    top: 10,
                    left: 10,
                    padding: "10px",
                    background: "white",
                    borderRadius: "5px",
                    zIndex: 10
                }}
            />

            {/* Three.js Scene */}
            <Canvas camera={{ position: [0, 2, 5] }}>
                <ambientLight intensity={0.5} />
                <directionalLight position={[10, 10, 10]} intensity={1} />
                <RoomModel setFloorHeight={setFloorHeight} />
                {uploadedModel && <UploadedModel modelUrl={uploadedModel} />}
                <OrbitControls />
            </Canvas>
        </div>
    );
}

export default App;
