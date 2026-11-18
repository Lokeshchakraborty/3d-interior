import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { RotateCw, Move, CheckCircle2, Box } from 'lucide-react';

export default function ThreeStage({ products = [], roomImage, onSelectProduct }) {
  const containerRef = useRef(null);
  const canvasRef = useRef(null);
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedProd, setSelectedProd] = useState(null);
  const sceneRef = useRef(null);
  const modelsRef = useRef([]);

  useEffect(() => {
    if (!canvasRef.current || !containerRef.current) return;

    const width = containerRef.current.clientWidth || 800;
    const height = containerRef.current.clientHeight || 550;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(46, width / height, 0.1, 100);
    camera.position.set(0, 2.4, 4.8);

    const renderer = new THREE.WebGLRenderer({
      canvas: canvasRef.current,
      alpha: true,
      antialias: true
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // 2. OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 + 0.02;
    controls.minDistance = 1.2;
    controls.maxDistance = 14.0;
    controls.target.set(0, 0.5, 0);

    // 3. Lighting & Shadows
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xfff5e6, 1.2);
    sunLight.position.set(-3.5, 6, 4.5);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    sunLight.shadow.bias = -0.001;
    scene.add(sunLight);

    const fillLight = new THREE.DirectionalLight(0xdbeafe, 0.4);
    fillLight.position.set(3, 4, -2);
    scene.add(fillLight);

    // 4. Ground Shadow Receiver & Subtle Grid
    const floorGeo = new THREE.PlaneGeometry(16, 16);
    const floorMat = new THREE.ShadowMaterial({ opacity: 0.35 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = 0;
    floor.receiveShadow = true;
    scene.add(floor);

    const grid = new THREE.GridHelper(8, 16, 0x38bdf8, 0x1e293b);
    grid.position.y = 0.001;
    grid.material.opacity = 0.3;
    grid.material.transparent = true;
    scene.add(grid);

    // 5. Load 3D Models
    const loader = new GLTFLoader();
    const loadedGroups = [];

    products.forEach((prod) => {
      const coords = prod.stage_coords || {};
      const xPct = coords.center_x_pct ?? (prod.hotspot?.x_pct || 50);
      const yPct = coords.center_y_pct ?? (prod.hotspot?.y_pct || 60);

      const posX = ((xPct - 50) / 50) * 2.8;
      const posZ = ((yPct - 50) / 50) * 2.2;

      const dim = prod.dimensions || {};
      const wM = Math.max(0.3, Math.min((dim.width_in || 48) * 0.0254, 3.5));
      const dM = Math.max(0.3, Math.min((dim.depth_in || 28) * 0.0254, 2.5));
      const hM = Math.max(0.02, Math.min((dim.height_in || 30) * 0.0254, 2.2));

      const modelUrl = prod.model_3d_url || `/api/model_3d/${prod.id}`;

      loader.load(
        modelUrl,
        (gltf) => {
          const root = gltf.scene;
          root.position.set(posX, 0, posZ);
          root.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });
          root.userData = prod;
          scene.add(root);
          loadedGroups.push(root);
        },
        undefined,
        () => {
          // Fallback procedural geometry
          const group = new THREE.Group();
          const geo = prod.category === 'rug' 
            ? new THREE.BoxGeometry(wM, 0.015, dM)
            : new THREE.BoxGeometry(wM, hM, dM);
          
          let mat;
          if (prod.cutout_url) {
            const tex = new THREE.TextureLoader().load(prod.cutout_url);
            mat = new THREE.MeshStandardMaterial({ map: tex, roughness: 0.6, transparent: true });
          } else {
            mat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.5 });
          }

          const mesh = new THREE.Mesh(geo, mat);
          mesh.position.y = hM / 2;
          mesh.castShadow = true;
          mesh.receiveShadow = true;
          group.add(mesh);
          group.position.set(posX, 0, posZ);
          group.userData = prod;
          scene.add(group);
          loadedGroups.push(group);
        }
      );
    });

    modelsRef.current = loadedGroups;

    // 6. Raycast Dragging & Selection
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let isDragging = false;
    let dragModel = null;
    const floorPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
    const planeIntersect = new THREE.Vector3();

    const onPointerDown = (e) => {
      const rect = canvasRef.current.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(modelsRef.current, true);

      if (intersects.length > 0) {
        let topGroup = intersects[0].object;
        while (topGroup.parent && topGroup.parent !== scene) {
          topGroup = topGroup.parent;
        }
        dragModel = topGroup;
        setSelectedModel(topGroup);
        setSelectedProd(topGroup.userData);
        if (onSelectProduct) onSelectProduct(topGroup.userData);

        // Highlight selection helper
        const oldHelper = scene.getObjectByName('selection-box');
        if (oldHelper) scene.remove(oldHelper);
        const bbox = new THREE.BoxHelper(topGroup, 0x38bdf8);
        bbox.name = 'selection-box';
        scene.add(bbox);

        if (e.button === 0 && !e.shiftKey) {
          isDragging = true;
          controls.enabled = false;
        }
      } else {
        const oldHelper = scene.getObjectByName('selection-box');
        if (oldHelper) scene.remove(oldHelper);
        setSelectedModel(null);
        setSelectedProd(null);
      }
    };

    const onPointerMove = (e) => {
      if (!isDragging || !dragModel) return;
      const rect = canvasRef.current.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      if (raycaster.ray.intersectPlane(floorPlane, planeIntersect)) {
        dragModel.position.x = Math.max(-3.5, Math.min(3.5, planeIntersect.x));
        dragModel.position.z = Math.max(-3.5, Math.min(3.5, planeIntersect.z));
        const helper = scene.getObjectByName('selection-box');
        if (helper) helper.update();
      }
    };

    const onPointerUp = () => {
      if (isDragging) {
        isDragging = false;
        controls.enabled = true;
      }
    };

    const canvasEl = canvasRef.current;
    canvasEl.addEventListener('pointerdown', onPointerDown);
    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerup', onPointerUp);

    // 7. Animation Loop
    let animId;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      controls.update();
      const helper = scene.getObjectByName('selection-box');
      if (helper) helper.update();
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      if (!containerRef.current || !renderer || !camera) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', handleResize);
      canvasEl.removeEventListener('pointerdown', onPointerDown);
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('pointerup', onPointerUp);
      renderer.dispose();
    };
  }, [products]);

  const handleRotate = () => {
    if (selectedModel && sceneRef.current) {
      selectedModel.rotation.y += Math.PI / 4;
      const helper = sceneRef.current.getObjectByName('selection-box');
      if (helper) helper.update();
    }
  };

  return (
    <div className="three-stage-wrapper" ref={containerRef}>
      <canvas ref={canvasRef} className="three-canvas" />

      {/* Floating 3D HUD */}
      <div className="three-hud">
        <div className="hud-pill">
          <span className="hud-dot"></span>
          <span>Left Drag: Orbit 3D &bull; Click Model: Move on Floor</span>
        </div>

        {selectedProd && (
          <div className="hud-selected-card">
            <div className="hud-info">
              <strong className="hud-title">{selectedProd.store} · {selectedProd.title?.slice(0, 22)}...</strong>
              <span className="hud-dim">
                {selectedProd.dimensions?.width_in}"W × {selectedProd.dimensions?.depth_in}"D × {selectedProd.dimensions?.height_in}"H
              </span>
            </div>
            <button type="button" onClick={handleRotate} className="hud-rotate-btn" title="Rotate 45°">
              <RotateCw size={14} />
              <span>Rotate 45°</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
