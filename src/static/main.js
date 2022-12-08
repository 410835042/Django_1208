import * as THREE from 'https://cdn.skypack.dev/three@0.130.0';
import { OrbitControls } from 'https://cdn.skypack.dev/three@0.130.0/examples/jsm/controls/OrbitControls.js'; //控制攝影機的模組
import { GLTFLoader } from 'https://cdn.skypack.dev/three@0.130.0/examples/jsm/loaders/GLTFLoader.js'; //匯入3D模型的模組
import { GUI } from 'https://cdn.skypack.dev/three@0.130.0/examples/jsm/libs/dat.gui.module';
//import Stats from 'https://cdn.skypack.dev/three/examples/jsm/libs/stats.module';
//import { createMeshes } from "https://cdn.skypack.dev/three@0.130.0/examples/jsm/loaders/meshes.js";

let hand_width = []
let hand_length = []
let palm = []
let hl1, hl2, hl3, hl4, hl5, pl = 0.0;
let hw1 , hw2 , hw3, hw4, hw5, pw = 0.0;


function ReadRatio(){
    fetch('/static/Ratio.txt')
        .then(response => response.text())
        .then(data => {
            // Do something with your data(string)
            const arr = data.split(/\r?\n/);  // arr (array)

            hand_width = arr[0].match(/\d+(?:\.\d+)?/g).map(Number)
            hand_length = arr[1].match(/\d+(?:\.\d+)?/g).map(Number)
            palm = arr[2].match(/\d+(?:\.\d+)?/g).map(Number)

            hl1 = hand_length[0]/4; hl2 = hand_length[1]/4; hl3 = hand_length[2]/4;hl4 = hand_length[3]/4; hl5 = hand_length[4]/4;
            hw1 = hand_width[0]/4; hw2 = hand_width[1]/4; hw3 = hand_width[2]/4; hw4 = hand_width[3]/4; hw5 = hand_width[4]/4;
            pl = palm[0]/4; pw = palm[1]/4;

            console.log(hand_width);
            console.log(hand_length);
            console.log(palm);
        })
        .catch(function(err) {
            console.log("尚無手部比例資訊，請點選「抓取手部比例」手部進行資訊的獲取")
        });
}

const thumb_l = document.getElementById( 'tl');
const index_l = document.getElementById( 'il');
const middle_l = document.getElementById( 'ml');
const ring_l = document.getElementById( 'rl');
const little_l = document.getElementById( 'll');
const palm_l = document.getElementById( 'pl');

const thumb_w = document.getElementById( 'tw');
const index_w = document.getElementById( 'iw');
const middle_w = document.getElementById( 'mw');
const ring_w = document.getElementById( 'rw');
const little_w = document.getElementById( 'lw');
const palm_w = document.getElementById( 'pw');

// console.log(Number(thumb_l.textContent)/4.0);
// console.log(thumb_w);

// const dt = document.getElementById( 'data' );
// dt.addEventListener( 'click', function () {
//     ReadRatio();
// })

ReadRatio();

/* 建立場景 */
const scene = new THREE.Scene(); //const 用來宣告常量
// scene.add(new THREE.AxesHelper(4));  // 在場景中增加xyz輔助線 红：X 绿：Y  蓝：Z，數字為線的長度
// const grid = new THREE.GridHelper(6, 6, 0xcccccc, 0xcccccc); // 增加網格(邊長, 邊長格數, 十字線顏色, 網格顏色)
// scene.add(grid);

const camera = new THREE.PerspectiveCamera( 25, window.innerWidth / window.innerHeight, 0.1, 1000 );
camera.position.set(0,3,20);


// 渲染器 {抗鋸齒、讓canvas包含alpha透明度} 放在畫布理
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, canvas: document.querySelector('canvas')});
renderer.setSize( window.innerWidth, window.innerHeight ); // 呈現在畫面的比例
renderer.setPixelRatio(devicePixelRatio);
renderer.setClearColor( 0x000000, 0 );
renderer.physicallyCorrectLights = true; // 物理正確光照：如同現實有漫射的光照
document.body.appendChild( renderer.domElement ); // 將canvas放入頁面

const controls = new OrbitControls( camera, renderer.domElement);
controls.enableDamping = true; // 增加慣性

const black = new THREE.Color(0x000000);
scene.background = black;

const back_Button = document.getElementById( 'back' ); //背景切換
back_Button.addEventListener( 'click', function () {
    if (scene.background == black){scene.background = null; console.log('transparent');}
    else{scene.background = black; console.log('black');}
});


/* 打光 */
const hemiLight = new THREE.HemisphereLight( 0xffffff, 0x444444, 3 );  // 半球燈
hemiLight.position.set( 0, 8, 0 );
scene.add( hemiLight );
// const hemiLighthelper = new THREE.HemisphereLightHelper( hemiLight );  // 半球燈
// scene.add( hemiLighthelper );

const dirLight1 = new THREE.DirectionalLight( 0xffffff, 3 ); // 定向燈
dirLight1.position.set( 8, 5, 8 );
scene.add( dirLight1 );
// const dirLightHelper = new THREE.DirectionalLightHelper( dirLight1 ); // 定向燈
// scene.add( dirLightHelper );

const dirLight2 = new THREE.DirectionalLight( 0xffffff, 3 ); // 定向燈
dirLight2.position.set( -8, 5, 8 );
scene.add( dirLight2 );
// const dirLightHelper2 = new THREE.DirectionalLightHelper( dirLight2 ); // 定向燈
// scene.add( dirLightHelper2 );

//主燈1
// const light1 = new THREE.PointLight(0xffffff,35); //0xc4c4c4黃燈
// light1.position.set(10,5,3);
// light1.castShadow = true;
// light1.shadow.mapSize.width = 1024;
// light1.shadow.mapSize.height = 1024;
// scene.add(light1);
//
// //打光 主燈2
// const light2 = new THREE.PointLight(0xffffff,35); //0xc4c4c4黃燈
// light2.position.set(-10,5,3);
// light2.castShadow = true;
// light2.shadow.mapSize.width = 1024;
// light2.shadow.mapSize.height = 1024;
// scene.add(light2);

/* Button */
const ml_Button = document.getElementById( 'man_l' );
const mr_Button = document.getElementById( 'man_r' );
const fl_Button = document.getElementById( 'female_l' );
const fr_Button = document.getElementById( 'female_r' );


/* 匯入3D模型 */
const man_hand_l = new GLTFLoader();
man_hand_l.load(
    '/static/Texture/man_hand_left/man_hand_left.gltf',
    function ( gltf ) {
        scene.add( gltf.scene );
        const m_hand = gltf.scene.children[1];

        m_hand.scale.set(0.7,0.7,0.7); //縮放(x,y,z)
        m_hand.rotation.set(0, 5, 0);//轉方向(x,y,z)
        m_hand.position.set(0,1,-3);

        const model = gltf.scene;
        model.visible=false;
        model.traverse(function(child){ if (child.name.indexOf("middle_1") != -1) {child.scale.set(1,1,1);} });
        // man_hand_gui("Rough Left Hand",m_hand, model); // gui

        if (hand_width.length>4 && hand_length.length>4 && palm.length>4){
            model.traverse(function(child){
                if (child.name.indexOf("thumb_1") != -1) {child.scale.set(
                    Number(thumb_w.textContent)/1.9, Number(thumb_l.textContent)/5.5, Number(thumb_l.textContent)/5.5);}
                if (child.name.indexOf("index_1") != -1) {child.scale.set(
                    Number(index_w.textContent)/1.6, Number(index_l.textContent)/6.5,Number(index_l.textContent)/6.5);}
                if (child.name.indexOf("middle_1") != -1) {child.scale.set(
                    Number(middle_w.textContent)/1.7, Number(middle_l.textContent)/7.0, Number(middle_l.textContent)/7.0);}
                if (child.name.indexOf("ring_1") != -1) {child.scale.set(
                    Number(ring_w.textContent)/1.6, Number(ring_l.textContent)/6.7, Number(ring_l.textContent)/6.7);}
                if (child.name.indexOf("little_1") != -1) {child.scale.set(
                    Number(little_w.textContent)/1.5, Number(little_l.textContent)/5.4, Number(little_l.textContent)/5.4);}
                if (child.name.indexOf("palme") != -1) {child.scale.set(
                    Number(palm_l.textContent)/7.7, 1, Number(palm_w.textContent)/9.8);}
            })
        }

        ml_Button.addEventListener( 'click', function (){
            if (model.visible == true){
                model.visible = false;
                ml_Button.style.background='#000000';
                ml_Button.style.color='#ffffff';
                mr_Button.removeAttribute("disabled");
                fr_Button.removeAttribute("disabled");
                fl_Button.removeAttribute("disabled");
            }
            else{
                model.visible = true;
                ml_Button.style.background='#ffffff';
                ml_Button.style.color='#000000';
                mr_Button.setAttribute("disabled","disabled");
                fr_Button.setAttribute("disabled","disabled");
                fl_Button.setAttribute("disabled","disabled");
            }
        } );
        // renderer.render( scene, camera );
      },
    undefined,
    function ( error ) { console.error( error ); }
);

const man_hand_r = new GLTFLoader();
man_hand_r.load(
    '/static/Texture/man_hand_right/man_hand_right.gltf',
    function ( gltf ) {
        scene.add( gltf.scene );
        const m_hand_r = gltf.scene.children[1];
        m_hand_r.rotation.set(0, 4.43, 0);//轉方向(x,y,z)
        m_hand_r.position.set(0,1,-3);
        m_hand_r.scale.set(0.7,0.7,-0.7); //縮放(x,y,z)

        const model = gltf.scene;
        model.visible=false;
        // man_hand_gui("Rough Right Hand",m_hand_r, model); // gui

        if (hand_width.length>4 && hand_length.length>4 && palm.length>4){
            model.traverse(function(child){
                if (child.name.indexOf("thumb_1") != -1) {child.scale.set(
                    Number(thumb_w.textContent)/1.9, Number(thumb_l.textContent)/5.5, Number(thumb_l.textContent)/5.5);}
                if (child.name.indexOf("index_1") != -1) {child.scale.set(
                    Number(index_w.textContent)/1.6, Number(index_l.textContent)/6.5,Number(index_l.textContent)/6.5);}
                if (child.name.indexOf("middle_1") != -1) {child.scale.set(
                    Number(middle_w.textContent)/1.7, Number(middle_l.textContent)/7.0, Number(middle_l.textContent)/7.0);}
                if (child.name.indexOf("ring_1") != -1) {child.scale.set(
                    Number(ring_w.textContent)/1.6, Number(ring_l.textContent)/6.7, Number(ring_l.textContent)/6.7);}
                if (child.name.indexOf("little_1") != -1) {child.scale.set(
                    Number(little_w.textContent)/1.5, Number(little_l.textContent)/5.4, Number(little_l.textContent)/5.4);}
                if (child.name.indexOf("palme") != -1) {child.scale.set(
                    Number(palm_l.textContent)/7.7, 1, Number(palm_w.textContent)/9.8);}
            })
        }

        mr_Button.addEventListener( 'click', function () {
            if (model.visible ==true){
                model.visible = false;
                mr_Button.style.background='#000000';
                mr_Button.style.color='#ffffff';
                ml_Button.removeAttribute("disabled");
                fr_Button.removeAttribute("disabled");
                fl_Button.removeAttribute("disabled");
            }
            else{
                model.visible = true;
                mr_Button.style.background='#ffffff';
                mr_Button.style.color='#000000';
                ml_Button.setAttribute("disabled","disabled");
                fr_Button.setAttribute("disabled","disabled");
                fl_Button.setAttribute("disabled","disabled");
            }
        } );
        // renderer.render( scene, camera );
      },
    undefined,
    function ( error ) { console.error( error ); }
);

const female_hand_l = new GLTFLoader();
female_hand_l.load(
    '/static/Texture/female_hand_left/female_hand_left.gltf',
    function ( gltf ) {
        scene.add( gltf.scene );
        const fh = gltf.scene.children[1]; //在scene下 新增一個子項目hand [1]是因為有模型本體加骨架兩項物件
        fh.scale.set(-1.8, 1.8, 1.8);
        fh.rotation.set(2, 0.037, 0.037);//轉方向(x,y,z)
        fh.position.set(0.1, 2.3, -2.5);
        const model = gltf.scene;
        model.visible=false;
        // f_hand_gui ("Delicate Left Hand",fh, model)


        if (hand_width.length>4 && hand_length.length>4 && palm.length>4){
            model.traverse(function(child){
                if (child.name.indexOf("thumb_1") != -1) {child.scale.set(
                    Number(thumb_w.textContent)/1.9, Number(thumb_l.textContent)/5.5, Number(thumb_l.textContent)/5.5);}
                if (child.name.indexOf("index_1") != -1) {child.scale.set(
                    Number(index_w.textContent)/1.6, Number(index_l.textContent)/6.5,Number(index_l.textContent)/6.5);}
                if (child.name.indexOf("middle_1") != -1) {child.scale.set(
                    Number(middle_w.textContent)/1.7, Number(middle_l.textContent)/7.0, Number(middle_l.textContent)/7.0);}
                if (child.name.indexOf("ring_1") != -1) {child.scale.set(
                    Number(ring_w.textContent)/1.6, Number(ring_l.textContent)/6.7, Number(ring_l.textContent)/6.7);}
                if (child.name.indexOf("little_1") != -1) {child.scale.set(
                    Number(little_w.textContent)/1.5, Number(little_l.textContent)/5.4, Number(little_l.textContent)/5.4);}
                if (child.name.indexOf("palme") != -1) {child.scale.set(
                    Number(palm_l.textContent)/7.7, 1, Number(palm_w.textContent)/9.8);}
            })
        }

        fl_Button.addEventListener( 'click', function () {
            if (model.visible ==true){
                model.visible = false;
                fl_Button.style.background='#000000';
                fl_Button.style.color='#ffffff';
                ml_Button.removeAttribute("disabled");
                mr_Button.removeAttribute("disabled");
                fr_Button.removeAttribute("disabled");
            }
            else{
                model.visible = true;
                fl_Button.style.background='#ffffff';
                fl_Button.style.color='#000000';
                ml_Button.setAttribute("disabled","disabled");
                mr_Button.setAttribute("disabled","disabled");
                fr_Button.setAttribute("disabled","disabled");
            }
        } );
        //renderer.render( scene, camera );delicate left hand
    },
    undefined,
    function ( error ) {
      console.error( error );
    }
);

const female_hand_r = new GLTFLoader();
female_hand_r.load(
    '/static/Texture/female_hand_right/female_hand_right.gltf',
    function ( gltf ) {
        scene.add( gltf.scene );
        const fh = gltf.scene.children[1]; //在scene下 新增一個子項目hand [1]是因為有模型本體加骨架兩項物件
        fh.scale.set(1.8, 1.8, 1.8);
        fh.rotation.set(2, 0, 0);//轉方向(x,y,z)
        fh.position.set(0.1, 2.3, -2.5);
        const model = gltf.scene;
        model.visible=false;
        // f_hand_gui ("Delicate Right Hand",fh, model)

        if (hand_width.length>4 && hand_length.length>4 && palm.length>4){
            model.traverse(function(child){
                if (child.name.indexOf("thumb_1") != -1) {child.scale.set(
                    Number(thumb_w.textContent)/1.9, Number(thumb_l.textContent)/5.5, Number(thumb_l.textContent)/5.5);}
                if (child.name.indexOf("index_1") != -1) {child.scale.set(
                    Number(index_w.textContent)/1.6, Number(index_l.textContent)/6.5,Number(index_l.textContent)/6.5);}
                if (child.name.indexOf("middle_1") != -1) {child.scale.set(
                    Number(middle_w.textContent)/1.7, Number(middle_l.textContent)/7.0, Number(middle_l.textContent)/7.0);}
                if (child.name.indexOf("ring_1") != -1) {child.scale.set(
                    Number(ring_w.textContent)/1.6, Number(ring_l.textContent)/6.7, Number(ring_l.textContent)/6.7);}
                if (child.name.indexOf("little_1") != -1) {child.scale.set(
                    Number(little_w.textContent)/1.5, Number(little_l.textContent)/5.4, Number(little_l.textContent)/5.4);}
                if (child.name.indexOf("palme") != -1) {child.scale.set(
                    Number(palm_l.textContent)/7.7, 1, Number(palm_w.textContent)/9.8);}
            })
        }

        fr_Button.addEventListener( 'click', function () {
            if (model.visible ==true){
                model.visible = false;
                fr_Button.style.background='#000000';
                fr_Button.style.color='#ffffff';
                ml_Button.removeAttribute("disabled");
                mr_Button.removeAttribute("disabled");
                fl_Button.removeAttribute("disabled");
            }
            else{
                model.visible = true;
                fr_Button.style.background='#ffffff';
                fr_Button.style.color='#000000';
                ml_Button.setAttribute("disabled","disabled");
                mr_Button.setAttribute("disabled","disabled");
                fl_Button.setAttribute("disabled","disabled");
            }
        } );
        //renderer.render( scene, camera );delicate left hand
    },
    undefined,
    function ( error ) {
      console.error( error );
    }
);

// const black_ring = new GLTFLoader();
// black_ring.load(
//     '/static/Texture/ring_gold/scene.gltf',
//     function ( gltf ) {
//         scene.add( gltf.scene );
//         const ring = gltf.scene.children[0]; //在scene下 新增一個子項目ring
//         ring.scale.set(0.023,0.023,0.023);
//         ring.rotation.set(0.6, 0.07, 0);//轉方向(x,y,z)
//         ring.position.x = -0.52;
//         ring.position.y = 0;
//         ring.position.z = 1.6;
//
//         const model = gltf.scene;
//         model.visible=false;
//         b_ring_gui(ring, model); // GUI
//         //renderer.render( scene, camera );
//     },
//     undefined,
//     function ( error ) { console.error( error ); }
// );
//
//
// const vilya_ring = new GLTFLoader();
// vilya_ring.load(
//     '/static/Texture/vilya_ring/scene.gltf',
//     function ( gltf ) {
//         scene.add( gltf.scene );
//         const v_ring = gltf.scene.children[0]; //在scene下 新增一個子項目ring
//         v_ring.scale.set(0.29, 0.29, 0.29);
//         v_ring.rotation.set(5.1, 0, 0.2);//轉方向(x,y,z)
//         v_ring.position.x = 0.79;
//         v_ring.position.y = 0.02;
//         v_ring.position.z = 2;
//
//         const model = gltf.scene;
//         model.visible=false;
//         v_ring_gui(v_ring, model); // GUI
//         //renderer.render( scene, camera );
//     },
//     undefined,
//     function ( error ) { console.error( error ); }
// );


/* 手指按鈕 */
const thumb = document.getElementById( 'thumb' );
const index = document.getElementById( 'index' );
const middle = document.getElementById( 'middle' );
const ring_f = document.getElementById( 'ring' );
const little = document.getElementById( 'little' );


/* 戒指模型載入 */
const ring_size = document.getElementById( 'r_size' );
var r_size = 0



const ring_gltf = document.getElementById( 'gltf' );
console.log(ring_gltf.textContent)

const ring_model = new GLTFLoader();
ring_model.load(
    ring_gltf.textContent,
    function ( gltf ) {
        scene.add( gltf.scene );
        const ring_part = gltf.scene.children[0]; //在scene下 新增一個子項目ring
        ring_part.scale.set(0.03, 0.03, 0.03);

        ring_size.addEventListener( 'click', function () {
            r_size = Number(ring_size.value)
            console.log(ring_size.value)
            ring_part.scale.set(r_size/467, r_size/467, r_size/467);
        })

        //wear_a_ring(ring_part)
        thumb.addEventListener( 'click', function () {
            if (thumb.hasAttribute("disabled")){
                thumb.style.background='#ffffff';
                thumb.style.color='#000000';
                index.setAttribute("disabled","disabled");
                middle.setAttribute("disabled","disabled");
                ring_f.setAttribute("disabled","disabled");
                little.setAttribute("disabled","disabled");
            }
            else{
                thumb.style.background='#000000';
                thumb.style.color='#ffffff';
                index.removeAttribute("disabled");
                middle.removeAttribute("disabled");
                ring_f.removeAttribute("disabled");
                little.removeAttribute("disabled");

                move_to_thumb(ring_part);
            }
        } );

        index.addEventListener( 'click', function () {
            if (index.hasAttribute("disabled")){
                index.style.background='#ffffff';
                index.style.color='#000000';
                thumb.setAttribute("disabled","disabled");
                middle.setAttribute("disabled","disabled");
                ring_f.setAttribute("disabled","disabled");
                little.setAttribute("disabled","disabled");
            }
            else{
                index.style.background='#000000';
                index.style.color='#ffffff';
                thumb.removeAttribute("disabled");
                middle.removeAttribute("disabled");
                ring_f.removeAttribute("disabled");
                little.removeAttribute("disabled");

                move_to_index(ring_part);
            }
        } );

        middle.addEventListener( 'click', function () {
            if (middle.hasAttribute("disabled")){
                middle.style.background='#ffffff';
                middle.style.color='#000000';
                thumb.setAttribute("disabled","disabled");
                index.setAttribute("disabled","disabled");
                ring_f.setAttribute("disabled","disabled");
                little.setAttribute("disabled","disabled");
            }
            else{
                middle.style.background='#000000';
                middle.style.color='#ffffff';
                thumb.removeAttribute("disabled");
                index.removeAttribute("disabled");
                ring_f.removeAttribute("disabled");
                little.removeAttribute("disabled");
                move_to_middle(ring_part);
            }
        } );

        ring_f.addEventListener( 'click', function () {
            if (ring_f.hasAttribute("disabled")){
                ring_f.style.background='#ffffff';
                ring_f.style.color='#000000';
                thumb.setAttribute("disabled","disabled");
                index.setAttribute("disabled","disabled");
                middle.setAttribute("disabled","disabled");
                little.setAttribute("disabled","disabled");
            }
            else{
                ring_f.style.background='#000000';
                ring_f.style.color='#ffffff';
                thumb.removeAttribute("disabled");
                index.removeAttribute("disabled");
                middle.removeAttribute("disabled");
                little.removeAttribute("disabled");
                move_to_ring(ring_part);
            }
        } );

        little.addEventListener( 'click', function () {
            if (little.hasAttribute("disabled")){
                little.style.background='#ffffff';
                little.style.color='#000000';
                thumb.setAttribute("disabled","disabled");
                index.setAttribute("disabled","disabled");
                middle.setAttribute("disabled","disabled");
                ring_f.setAttribute("disabled","disabled");
            }
            else{
                little.style.background='#000000';
                little.style.color='#ffffff';
                thumb.removeAttribute("disabled");
                index.removeAttribute("disabled");
                middle.removeAttribute("disabled");
                ring_f.removeAttribute("disabled");
                move_to_little(ring_part);
            }
        } );
    },
    undefined,
    function ( error ) { console.error( error ); }
);



/* 戒指模型配戴函示 */
function move_to_thumb(ring) {
    if (mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.92, 0, 0);//轉方向(x,y,z)
        ring.position.x = -1.31;
        ring.position.y = -0.45;
        ring.position.z = 0.35;
    } else if (ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.92, 0, 0);//轉方向(x,y,z)
        ring.position.x = 1.31;
        ring.position.y = -0.45;
        ring.position.z = 0.35;
    } else if (ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.34, 0.61, 0);//轉方向(x,y,z)
        ring.position.x = 1.31;
        ring.position.y = 0.13;
        ring.position.z = 0.59;
    } else if (ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.42, -0.6, 0);//轉方向(x,y,z)
        ring.position.x = -1.27;
        ring.position.y = 0.08;
        ring.position.z = 0.57;
    }
}

function move_to_index(ring) {
    if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.6, 0.07, 0);//轉方向(x,y,z)
        ring.position.x = -0.52;
        ring.position.y = 0;
        ring.position.z = 1.6;
    }
    else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.6, -0.07, 0);//轉方向(x,y,z)
        ring.position.x = 0.55;
        ring.position.y = 0;
        ring.position.z = 1.6;
    }
    else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.38, 0.12, 0);//轉方向(x,y,z)
        ring.position.x = 0.75;
        ring.position.y = 0.12;
        ring.position.z = 1.8;
    }
    else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.38, -0.25, 0);//轉方向(x,y,z)
        ring.position.x = -0.72;
        ring.position.y = 0.07;
        ring.position.z = 1.8;
    }
}

function move_to_middle(ring) {
    if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.81, 0.14, 0);//轉方向(x,y,z)
        ring.position.x = 0.03;
        ring.position.y = -0.1;
        ring.position.z = 1.52;
    }
    else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.81, -0.14, 0);//轉方向(x,y,z)
        ring.position.x = -0.01;
        ring.position.y = -0.1;
        ring.position.z = 1.52;
    }
    else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.5, 0.08, 0);//轉方向(x,y,z)
        ring.position.x = 0.16;
        ring.position.y = 0.08;
        ring.position.z = 2;
    }
    else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.42, -0.14, 0);//轉方向(x,y,z)
        ring.position.x = -0.14;
        ring.position.y = 0.065;
        ring.position.z = 1.98;
    }
}

function move_to_ring(ring) {
    if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.81, 0.2, 0);//轉方向(x,y,z)
        ring.position.x = 0.5;
        ring.position.y = -0.13;
        ring.position.z = 1.19;
    }
    else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.81, -0.2, 0);//轉方向(x,y,z)
        ring.position.x = -0.52;
        ring.position.y = -0.13;
        ring.position.z = 1.19;
    }
    else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.64, 0.01, 0);//轉方向(x,y,z)
        ring.position.x = -0.39;
        ring.position.y = -0.11;
        ring.position.z = 1.84;
    }
    else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.61, 0.05, 0);//轉方向(x,y,z)
        ring.position.x = 0.41;
        ring.position.y = -0.12;
        ring.position.z = 1.87;
    }
}

function move_to_little(ring) {
    if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.84, 0.31, 0);//轉方向(x,y,z)
        ring.position.x = 0.935;
        ring.position.y = -0.28;
        ring.position.z = 0.91;
    }
    else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.84, -0.31, 0);//轉方向(x,y,z)
        ring.position.x = -0.91;
        ring.position.y = -0.28;
        ring.position.z = 0.91;
    }
    else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.61, -0.25, 0);//轉方向(x,y,z)
        ring.position.x = -0.99;
        ring.position.y = -0.11;
        ring.position.z = 1.45;
    }
    else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
        // ring.scale.set(0.03, 0.03, 0.03);
        ring.rotation.set(0.61, 0.05, 0);//轉方向(x,y,z)
        ring.position.x = 1.06;
        ring.position.y = -0.13;
        ring.position.z = 1.55;
    }
}


const gold_Button = document.getElementById( 'gold' );
const silver_Button = document.getElementById( 'silver' );
const rose_gold_Button = document.getElementById( 'rose_gold' );



/* 建立控致面板 */
// const gui = new GUI({ width: 300 }); //GUI母體
// // man_hand's gui
//
// function man_hand_gui (name, m_hand, model){
//     const Man_hand = gui.addFolder(name);
//     const folder1 = Man_hand.addFolder("scale");
//     const folder2 = Man_hand.addFolder("Thumb Finger"); const folder2x = folder2.addFolder("Thumb Finger - X"); const folder2y = folder2.addFolder("Thumb Finger - Y");
//     const folder3 = Man_hand.addFolder("Index Finger"); const folder3x = folder3.addFolder("Index Finger - X"); const folder3y = folder3.addFolder("Index Finger - Y");
//     const folder4 = Man_hand.addFolder("Middle Finger"); const folder4x = folder4.addFolder("Middle Finger - X"); const folder4y = folder4.addFolder("Middle Finger - Y");
//     const folder5 = Man_hand.addFolder("Ring Finger"); const folder5x = folder5.addFolder("Ring Finger - X"); const folder5y = folder5.addFolder("Ring Finger - Y");
//     const folder6 = Man_hand.addFolder("Little Finger"); const folder6x = folder6.addFolder("Little Finger - X"); const folder6y = folder6.addFolder("Little Finger - Y");
//     //Man_hand.open();
//     const palette = {
//         color1: '#FF0000', // CSS string
//         color2: [ 0, 128, 255 ], // RGB array
//     };
//     folder1.open();
//     folder2x.open(); folder2y.open();
//     folder3x.open(); folder3y.open();
//     folder4x.open(); folder4y.open();
//     folder5x.open(); folder5y.open();
//     folder6x.open(); folder6y.open();
//
//     const setting = { "show model": false};
//     folder1.add(setting, "show model").onChange((visible) => { model.visible = visible; });
//     folder1.add(m_hand.rotation, 'x', 0, 8).name('scale X Axis');
//     folder1.add(m_hand.rotation, 'y', 0, 8).name('scale Y Axis');
//     folder1.add(m_hand.rotation, 'z', 0, 8).name('scale Z Axis');
//     // folder1.addColor(palette, 'color1').name('Color HEX');
//     // folder1.addColor(palette, 'color2').name('Color RGB');
//
//     model.traverse(function(child){
//         if (child.name.indexOf("thumb_1") != -1) {folder2x.add(child.scale, 'z', 0, 2).name('thumb_1' ); folder2y.add(child.scale, 'y', 0, 3).name('thumb_1' );}
//         if (child.name.indexOf("thumb_2") != -1) {folder2x.add(child.scale, 'z', 0, 2).name('thumb_2' ); folder2y.add(child.scale, 'y', 0, 3).name('thumb_2' );}
//
//         if (child.name.indexOf("palm") != -1) {folder3x.add(child.scale, 'z', 0, 3).name('palm_y' ); folder3x.add(child.scale, 'x', 0, 3).name('palm_x' );}
//
//         if (child.name.indexOf("index_1") != -1) {folder3x.add(child.scale, 'z', 0, 2).name('index_1' ); folder3y.add(child.scale, 'y', 0, 3).name('index_1' );}
//         if (child.name.indexOf("index_2") != -1) {folder3x.add(child.scale, 'z', 0, 2).name('index_2' ); folder3y.add(child.scale, 'y', 0, 3).name('index_2' );}
//         if (child.name.indexOf("index_3") != -1) {folder3x.add(child.scale, 'z', 0, 2).name('index_3' ); folder3y.add(child.scale, 'y', 0, 3).name('index_3' );}
//
//         if (child.name.indexOf("middle_1") != -1) {folder4x.add(child.scale, 'z', 0, 2).name('middle_1' ); folder4y.add(child.scale, 'y', 0, 3).name('middle_1' );}
//         if (child.name.indexOf("middle_2") != -1) {folder4x.add(child.scale, 'z', 0, 2).name('middle_2' ); folder4y.add(child.scale, 'y', 0, 3).name('middle_2' );}
//         if (child.name.indexOf("middle_3") != -1) {folder4x.add(child.scale, 'z', 0, 2).name('middle_3' ); folder4y.add(child.scale, 'y', 0, 3).name('middle_3' );}
//
//         if (child.name.indexOf("ring_1") != -1) {folder5x.add(child.scale, 'z', 0, 2).name('ring_1' ); folder5y.add(child.scale, 'y', 0, 3).name('ring_1' );}
//         if (child.name.indexOf("ring_2") != -1) {folder5x.add(child.scale, 'z', 0, 2).name('ring_2' ); folder5y.add(child.scale, 'y', 0, 3).name('ring_2' );}
//         if (child.name.indexOf("ring_3") != -1) {folder5x.add(child.scale, 'z', 0, 2).name('ring_3' ); folder5y.add(child.scale, 'y', 0, 3).name('ring_3' );}
//
//         if (child.name.indexOf("little_1") != -1) {folder6x.add(child.scale, 'z', 0, 2).name('little_1' ); folder6y.add(child.scale, 'y', 0, 3).name('little_1' );}
//         if (child.name.indexOf("little_2") != -1) {folder6x.add(child.scale, 'z', 0, 2).name('little_2' ); folder6y.add(child.scale, 'y', 0, 3).name('little_2' );}
//         if (child.name.indexOf("little_3") != -1) {folder6x.add(child.scale, 'z', 0, 2).name('little_3' ); folder6y.add(child.scale, 'y', 0, 3).name('little_3' );}
//     })
// }
//
// // female_hand's gui
// function f_hand_gui (name, f_hand, model) {
//     const Female_hand = gui.addFolder(name);
//     const folder1 = Female_hand.addFolder("Scale");
//     // const folder2 = Female_hand.addFolder("Rotation");
//     const folder2 = Female_hand.addFolder("Thumb Finger"); const folder2x = folder2.addFolder("Thumb Finger - X"); const folder2y = folder2.addFolder("Thumb Finger - Y");
//     const folder3 = Female_hand.addFolder("Index Finger"); const folder3x = folder3.addFolder("Index Finger - X"); const folder3y = folder3.addFolder("Index Finger - Y");
//     const folder4 = Female_hand.addFolder("Middle Finger"); const folder4x = folder4.addFolder("Middle Finger - X"); const folder4y = folder4.addFolder("Middle Finger - Y");
//     const folder5 = Female_hand.addFolder("Ring Finger"); const folder5x = folder5.addFolder("Ring Finger - X"); const folder5y = folder5.addFolder("Ring Finger - Y");
//     const folder6 = Female_hand.addFolder("Little Finger"); const folder6x = folder6.addFolder("Little Finger - X"); const folder6y = folder6.addFolder("Little Finger - Y");
//     //Female_hand.open();
//     folder1.open();
//     // folder2.open();
//     folder2x.open(); folder2y.open();
//     folder3x.open(); folder3y.open();
//     folder4x.open(); folder4y.open();
//     folder5x.open(); folder5y.open();
//     folder6x.open(); folder6y.open();
//
//     const setting = {"show model": false,};
//     folder1.add(setting, "show model").onChange((visible) => { model.visible = visible; });
//     folder1.add(f_hand.rotation, 'x', 0, 8, 0.001).name('scale X Axis');
//     folder1.add(f_hand.rotation, 'y', 0, 8, 0.001).name('scale Y Axis');
//     folder1.add(f_hand.rotation, 'z', 0, 8, 0.001).name('scale Z Axis');
//     // folder1.add(f_hand.scale, 'x', 0.1, 1).name('Scale X Axis');
//     // folder2.add(f_hand.rotation, 'x', 0, Math.PI*2).name('Rotation X Axis');
//     // folder3.add(f_hand.position, 'x', -10, 10).name('Position X Axis');
//
//     model.traverse(function(child){
//         if (child.name.indexOf("thumb_1") != -1) {
//             folder2x.add(child.scale, 'x', 0, 2).name('thumb_1' );
//             folder2y.add(child.scale, 'y', 0, 3).name('thumb_1' );
//         }
//         if (child.name.indexOf("thumb_2") != -1) {
//             folder2x.add(child.scale, 'x', 0, 2).name('thumb_2' );
//             folder2y.add(child.scale, 'y', 0, 3).name('thumb_2' );
//         }
//
//         if (child.name.indexOf("palm") != -1) {
//             folder3x.add(child.scale, 'y', 0, 3).name('palm_y' );
//             folder3x.add(child.scale, 'x', 0, 3).name('palm_x' );
//         }
//         if (child.name.indexOf("index_1") != -1) {
//             folder3x.add(child.scale, 'x', 0, 2).name('index_1' );
//             folder3y.add(child.scale, 'y', 0, 3).name('index_1' );
//         }
//         if (child.name.indexOf("index_2") != -1) {
//             folder3x.add(child.scale, 'x', 0, 2).name('index_2' );
//             folder3y.add(child.scale, 'y', 0, 3).name('index_2' );
//         }
//         if (child.name.indexOf("index_3") != -1) {
//             folder3x.add(child.scale, 'x', 0, 2).name('index_3' );
//             folder3y.add(child.scale, 'y', 0, 3).name('index_3' );
//         }
//
//         if (child.name.indexOf("middle_1") != -1) {
//             folder4x.add(child.scale, 'x', 0, 2).name('middle_1' );
//             folder4y.add(child.scale, 'y', 0, 3).name('middle_1' );
//         }
//         if (child.name.indexOf("middle_2") != -1) {
//             folder4x.add(child.scale, 'x', 0, 2).name('middle_2' );
//             folder4y.add(child.scale, 'y', 0, 3).name('middle_2' );
//         }
//         if (child.name.indexOf("middle_3") != -1) {
//             folder4x.add(child.scale, 'x', 0, 2).name('middle_3' );
//             folder4y.add(child.scale, 'y', 0, 3).name('middle_3' );
//         }
//
//         if (child.name.indexOf("ring_1") != -1) {
//             folder5x.add(child.scale, 'x', 0, 2).name('ring_1' );
//             folder5y.add(child.scale, 'y', 0, 3).name('ring_1' );
//         }
//         if (child.name.indexOf("ring_2") != -1) {
//             folder5x.add(child.scale, 'x', 0, 2).name('ring_2' );
//             folder5y.add(child.scale, 'y', 0, 3).name('ring_2' );
//         }
//         if (child.name.indexOf("ring_3") != -1) {
//             folder5x.add(child.scale, 'x', 0, 2).name('ring_3' );
//             folder5y.add(child.scale, 'y', 0, 3).name('ring_3' );
//         }
//
//         if (child.name.indexOf("little_1") != -1) {
//             folder6x.add(child.scale, 'x', 0, 2).name('little_1' );
//             folder6y.add(child.scale, 'y', 0, 3).name('little_1' );
//         }
//         if (child.name.indexOf("little_2") != -1) {
//             folder6x.add(child.scale, 'x', 0, 2).name('little_2' );
//             folder6y.add(child.scale, 'y', 0, 3).name('little_2' );
//         }
//         if (child.name.indexOf("little_3") != -1) {
//             folder6x.add(child.scale, 'x', 0, 2).name('little_3' );
//             folder6y.add(child.scale, 'y', 0, 3).name('little_3' );
//         }
//     })
//
// }
//
//
// // ring's gui
// function b_ring_gui(ring, model) {
//     const Back_Ring = gui.addFolder("Back Ring");
//     const folder1 = Back_Ring.addFolder("Scale");
//     // const folder2 = Back_Ring.addFolder("Rotation");
//     // const folder3 = Back_Ring.addFolder("Position");
//     const folder4 = Back_Ring.addFolder("Hand");
//     const put = {
//         'Thumb': movetothumb,
//         'Index': movetoindex,
//         'Middle': movetomiddle,
//         'Ring': movetoring,
//         'Little': movetolittle
//     };
//     //Back_Ring.open();
//     folder1.open();
//     // folder2.open();
//     // folder3.open();
//     folder4.open();
//
//     const setting = { "show model": false };
//
//     folder1.add(setting, "show model").onChange((visible) => { model.visible = visible; });
//     // folder1.add(ring.scale, 'x', 0.01, 0.05).name('Scale X Axis');
//     // folder1.add(ring.scale, 'y', 0.01, 0.05).name('Scale Y Axis');
//     // folder1.add(ring.scale, 'z', 0.01, 0.05).name('Scale Z Axis');
//     //
//     // folder2.add(ring.rotation, 'x', -1, Math.PI, 0.01).name('Rotation X Axis');
//     // folder2.add(ring.rotation, 'y', -1, Math.PI, 0.01).name('Rotation Y Axis');
//     // folder2.add(ring.rotation, 'z', -1, Math.PI, 0.01).name('Rotation Z Axis');
//     //
//     // folder3.add(ring.position, 'x', -3, 3, 0.01).name('Position X Axis').listen();
//     // folder3.add(ring.position, 'y', -3, 3, 0.01).name('Position Y Axis');
//     // folder3.add(ring.position, 'z', -3, 3, 0.01).name('Position Z Axis');
//
//     folder4.add(put, 'Thumb').name('Thumb');
//     folder4.add(put, 'Index').name('Index');
//     folder4.add(put, 'Middle').name('Middle');
//     folder4.add(put, 'Ring').name('Ring');
//     folder4.add(put, 'Little').name('Little');
//
//     function movetothumb(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             ring.scale.set(0.024,0.024,0.024);
//             ring.rotation.set(0.92, 0, 0);//轉方向(x,y,z)
//             ring.position.x = -1.31;
//             ring.position.y = -0.45;
//             ring.position.z = 0.35;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.024,0.024,0.024);
//             ring.rotation.set(0.92, 0, 0);//轉方向(x,y,z)
//             ring.position.x = 1.31;
//             ring.position.y = -0.45;
//             ring.position.z = 0.35;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.024,0.024,0.024);
//             ring.rotation.set(0.34, 0.61, 0);//轉方向(x,y,z)
//             ring.position.x = 1.31;
//             ring.position.y = 0.13;
//             ring.position.z = 0.59;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.022,0.022,0.022);
//             ring.rotation.set(0.42, -0.6, 0);//轉方向(x,y,z)
//             ring.position.x = -1.27;
//             ring.position.y = 0.08;
//             ring.position.z = 0.57;
//         }
//     }
//
//     function movetoindex(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             ring.scale.set(0.023,0.023,0.023);
//             ring.rotation.set(0.6, 0.07, 0);//轉方向(x,y,z)
//             ring.position.x = -0.52;
//             ring.position.y = 0;
//             ring.position.z = 1.6;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.023,0.023,0.023);
//             ring.rotation.set(0.6, -0.07, 0);//轉方向(x,y,z)
//             ring.position.x = 0.55;
//             ring.position.y = 0;
//             ring.position.z = 1.6;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.023,0.023,0.023);
//             ring.rotation.set(0.38, 0.12, 0);//轉方向(x,y,z)
//             ring.position.x = 0.75;
//             ring.position.y = 0.12;
//             ring.position.z = 1.8;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.023,0.023,0.023);
//             ring.rotation.set(0.38, -0.25, 0);//轉方向(x,y,z)
//             ring.position.x = -0.72;
//             ring.position.y = 0.07;
//             ring.position.z = 1.8;
//         }
//
//     }
//
//     function movetomiddle(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             ring.scale.set(0.023,0.023,0.023);
//             ring.rotation.set(0.81, 0.14, 0);//轉方向(x,y,z)
//             ring.position.x = 0.03;
//             ring.position.y = -0.1;
//             ring.position.z = 1.52;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.023,0.023,0.023);
//             ring.rotation.set(0.81, -0.14, 0);//轉方向(x,y,z)
//             ring.position.x = -0.01;
//             ring.position.y = -0.1;
//             ring.position.z = 1.52;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.022,0.022,0.022);
//             ring.rotation.set(0.5, 0.08, 0);//轉方向(x,y,z)
//             ring.position.x = 0.16;
//             ring.position.y = 0.08;
//             ring.position.z = 2;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.022,0.022,0.022);
//             ring.rotation.set(0.42, -0.14, 0);//轉方向(x,y,z)
//             ring.position.x = -0.14;
//             ring.position.y = 0.065;
//             ring.position.z = 1.98;
//         }
//     }
//
//     function movetoring(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             ring.scale.set(0.021,0.021,0.021);
//             ring.rotation.set(0.81, 0.2, 0);//轉方向(x,y,z)
//             ring.position.x = 0.5;
//             ring.position.y = -0.13;
//             ring.position.z = 1.19;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.021,0.021,0.021);
//             ring.rotation.set(0.81, -0.2, 0);//轉方向(x,y,z)
//             ring.position.x = -0.52;
//             ring.position.y = -0.13;
//             ring.position.z = 1.19;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.021,0.021,0.021);
//             ring.rotation.set(0.64, 0.01, 0);//轉方向(x,y,z)
//             ring.position.x = -0.39;
//             ring.position.y = -0.11;
//             ring.position.z = 1.84;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.021,0.021,0.021);
//             ring.rotation.set(0.61, 0.05, 0);//轉方向(x,y,z)
//             ring.position.x = 0.41;
//             ring.position.y = -0.12;
//             ring.position.z = 1.87;
//         }
//     }
//
//     function movetolittle(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             ring.scale.set(0.0175,0.0175,0.0175);
//             ring.rotation.set(0.84, 0.31, 0);//轉方向(x,y,z)
//             ring.position.x = 0.935;
//             ring.position.y = -0.28;
//             ring.position.z = 0.91;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.0175,0.0175,0.0175);
//             ring.rotation.set(0.84, -0.31, 0);//轉方向(x,y,z)
//             ring.position.x = -0.91;
//             ring.position.y = -0.28;
//             ring.position.z = 0.91;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.019,0.019,0.019);
//             ring.rotation.set(0.61, -0.25, 0);//轉方向(x,y,z)
//             ring.position.x = -0.99;
//             ring.position.y = -0.11;
//             ring.position.z = 1.45;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             ring.scale.set(0.019,0.019,0.019);
//             ring.rotation.set(0.61, 0.05, 0);//轉方向(x,y,z)
//             ring.position.x = 1.06;
//             ring.position.y = -0.13;
//             ring.position.z = 1.55;
//         }
//
//     }
// }
//
// function v_ring_gui(v_ring, model) {
//     const v_Ring = gui.addFolder("Vilya Ring");
//     const folder1 = v_Ring.addFolder("Scale");
//     // const folder2 = v_Ring.addFolder("Rotation");
//     // const folder3 = v_Ring.addFolder("Position");
//     const folder4 = v_Ring.addFolder("Finger");
//     const put = {
//         'Thumb': movetothumb,
//         'Index': movetoindex,
//         'Middle': movetomiddle,
//         'Ring': movetoring,
//         'Little': movetolittle
//     };
//
//     //Back_Ring.open();
//     folder1.open();
//     // folder2.open();
//     // folder3.open();
//     folder4.open();
//
//     const setting = { "show model": false };
//
//     folder1.add(setting, "show model").onChange((visible) => { model.visible = visible; });
//     // folder1.add(v_ring.scale, 'x', 0.01, 1).name('Scale X Axis');
//     // folder1.add(v_ring.scale, 'y', 0.01, 1).name('Scale Y Axis');
//     // folder1.add(v_ring.scale, 'z', 0.01, 1).name('Scale Z Axis');
//     //
//     // folder2.add(v_ring.rotation, 'x', -1, Math.PI*2, 0.01).name('Rotation X Axis');
//     // folder2.add(v_ring.rotation, 'y', -1, Math.PI*2, 0.01).name('Rotation Y Axis');
//     // folder2.add(v_ring.rotation, 'z', -1, Math.PI*2, 0.10).name('Rotation Z Axis');
//     //
//     // folder3.add(v_ring.position, 'x', -3, 3, 0.01).name('Position X Axis');
//     // folder3.add(v_ring.position, 'y', -3, 3, 0.01).name('Position Y Axis');
//     // folder3.add(v_ring.position, 'z', -3, 3, 0.01).name('Position Z Axis');
//
//     folder4.add(put, 'Thumb').name('Thumb');
//     folder4.add(put, 'Index').name('Index');
//     folder4.add(put, 'Middle').name('Middle');
//     folder4.add(put, 'Ring').name('Ring');
//     folder4.add(put, 'Little').name('Little');
//
//     function movetothumb(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             v_ring.scale.set(0.3, 0.3, 0.3);
//             v_ring.rotation.set(2.42, 4.26, -0.1);//轉方向(x,y,z)
//             v_ring.position.x = -1.2;
//             v_ring.position.y = -0.56;
//             v_ring.position.z = 0.41;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.3, 0.3, 0.3);
//             v_ring.rotation.set(-0.61, 1.23, 0);//轉方向(x,y,z)
//             v_ring.position.x = 1.31;
//             v_ring.position.y = -0.51;
//             v_ring.position.z = 0.38;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.28, 0.28, 0.28);
//             v_ring.rotation.set(4.3, 0.7, 4.1);//轉方向(x,y,z)
//             v_ring.position.x = 1.39;
//             v_ring.position.y = 0.09;
//             v_ring.position.z = 0.68;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.28, 0.28, 0.28);
//             v_ring.rotation.set(1.36, 3.74, 2.3);//轉方向(x,y,z)
//             v_ring.position.x = -1.3;
//             v_ring.position.y = 0.06;
//             v_ring.position.z = 0.6;
//         }
//
//     }
//
//     function movetoindex(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             v_ring.scale.set(0.3, 0.3, 0.3);
//             v_ring.rotation.set(-1, 0.12, 0.1);//轉方向(x,y,z)
//             v_ring.position.x = -0.52;
//             v_ring.position.y = -0.06;
//             v_ring.position.z = 1.65;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.3, 0.3, 0.3);
//             v_ring.rotation.set(-1, -0.15, 0);//轉方向(x,y,z)
//             v_ring.position.x = 0.54;
//             v_ring.position.y = -0.06;
//             v_ring.position.z = 1.65;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.29, 0.29, 0.29);
//             v_ring.rotation.set(5.1, 0, 0.2);//轉方向(x,y,z)
//             v_ring.position.x = 0.78;
//             v_ring.position.y = 0.02;
//             v_ring.position.z = 2;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.29, 0.29, 0.29);
//             v_ring.rotation.set(5.1, 0, -0.2);//轉方向(x,y,z)
//             v_ring.position.x = -0.78;
//             v_ring.position.y = -0.02;
//             v_ring.position.z = 2;
//         }
//     }
//
//     function movetomiddle(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             v_ring.scale.set(0.27, 0.27, 0.27);
//             v_ring.rotation.set(-0.87, 0.31, 0.2);//轉方向(x,y,z)
//             v_ring.position.x = 0.045;
//             v_ring.position.y = -0.13;
//             v_ring.position.z = 1.57;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.27, 0.27, 0.27);
//             v_ring.rotation.set(-0.74, -0.41, -0.1);//轉方向(x,y,z)
//             v_ring.position.x = -0.02;
//             v_ring.position.y = -0.13;
//             v_ring.position.z = 1.55;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.28, 0.28, 0.28);
//             v_ring.rotation.set(5.21, 0, 0.1);//轉方向(x,y,z)
//             v_ring.position.x = 0.18;
//             v_ring.position.y = 0.02;
//             v_ring.position.z = 2.1;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.28, 0.28, 0.28);
//             v_ring.rotation.set(5.21, 0, -0.15);//轉方向(x,y,z)
//             v_ring.position.x = -0.16;
//             v_ring.position.y = 0.02;
//             v_ring.position.z = 2.1;
//         }
//     }
//
//     function movetoring(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             v_ring.scale.set(0.26, 0.26, 0.26);
//             v_ring.rotation.set(-0.87, 0.31, 0.25);//轉方向(x,y,z)
//             v_ring.position.x = 0.56;
//             v_ring.position.y = -0.25;
//             v_ring.position.z = 1.3;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.26, 0.26, 0.26);
//             v_ring.rotation.set(-0.74, -0.41, -0.1);//轉方向(x,y,z)
//             v_ring.position.x = -0.54;
//             v_ring.position.y = -0.25;
//             v_ring.position.z = 1.3;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.27, 0.27, 0.27);
//             v_ring.rotation.set(5.44, 0, 3.1);//轉方向(x,y,z)
//             v_ring.position.x = -0.39;
//             v_ring.position.y = -0.13;
//             v_ring.position.z = 1.88;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.27, 0.27, 0.27);
//             v_ring.rotation.set(5.44, 0, 3.1);//轉方向(x,y,z)
//             v_ring.position.x = 0.42;
//             v_ring.position.y = -0.1;
//             v_ring.position.z = 1.9;
//         }
//     }
//
//     function movetolittle(){
//         if(mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")){
//             v_ring.scale.set(0.23, 0.23, 0.23);
//             v_ring.rotation.set(-0.87, 0.51, 0.3);//轉方向(x,y,z)
//             v_ring.position.x = 0.93;
//             v_ring.position.y = -0.28;
//             v_ring.position.z = 0.9;
//         }
//         else if(ml_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.225, 0.225, 0.225);
//             v_ring.rotation.set(-0.87, -0.54, -0.3);//轉方向(x,y,z)
//             v_ring.position.x = -0.915;
//             v_ring.position.y = -0.275;
//             v_ring.position.z = 0.91;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fl_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.25, 0.25, 0.25);
//             v_ring.rotation.set(5.38, 0, 2.9);//轉方向(x,y,z)
//             v_ring.position.x = -1.01;
//             v_ring.position.y = -0.11;
//             v_ring.position.z = 1.49;
//         }
//         else if(ml_Button.hasAttribute("disabled") && mr_Button.hasAttribute("disabled") && fr_Button.hasAttribute("disabled")) {
//             v_ring.scale.set(0.25, 0.25, 0.25);
//             v_ring.rotation.set(-1, 0.51, 0.25);//轉方向(x,y,z)
//             v_ring.position.x = 1.08;
//             v_ring.position.y = -0.15;
//             v_ring.position.z = 1.6;
//         }
//
//     }
// }
//
//


/* 持續活動 */
let mixer;
const clock = new THREE.Clock();

function  animate(){
    requestAnimationFrame( animate );
    // sphere.rotation.x += 0.005;
    // sphere.rotation.y += 0.005;


    if (mixer) { mixer.update(clock.getDelta()); }  // 推動混合器時間 --> 更新動畫
    renderer.render( scene, camera );
}
animate();
