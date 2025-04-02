import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);


const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(1, 1, 1).normalize();
scene.add(light);

const gltfLoader = new GLTFLoader();
const url = '/static/drevo.glb';

gltfLoader.load(url, (gltf) => {
    const root = gltf.scene;
    console.log("Model naložen:", root);
    root.position.set(0, 0, 0);
    root.scale.set(1, 1, 1);
    scene.add(root);
}, undefined, (error) => {
    console.error("Napaka pri nalaganju modela:", error);
});

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

camera.position.set(0, 2, 5);

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

animate();
