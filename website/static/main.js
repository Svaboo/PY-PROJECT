import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(5, 10, 7.5);
directionalLight.castShadow = true;
scene.add(directionalLight);

const gltfLoader = new GLTFLoader();
const url = '/static/map.glb';

gltfLoader.load(url, (gltf) => {
    const root = gltf.scene;
    console.log("Model naložen:", root);
    root.position.set(0, 0, 0);
    root.scale.set(1, 1, 1);
    scene.add(root);
}, undefined, (error) => {
    console.error("Napaka pri nalaganju modela:", error);
});

camera.position.x = -6.440;
camera.position.y = 17.907790044514503;
camera.position.z = -34.640789754832838;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

function animate() {

    console.log(camera.position);
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

animate();
