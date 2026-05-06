
const API={
  products:"/api/products",
  auth:"/api/auth",
  user:"/api/users",
  orders:"/api/orders"
};

let state={user:null,cart:[]};
const app=document.getElementById("app");
const nav=document.getElementById("nav");

function renderNav(){
  nav.innerHTML=state.user?
  `
    <button onclick="loadProducts()">Store</button>
    <button onclick="showCart()">Cart (${state.cart.length})</button>
    <button onclick="showCreateProduct()">Add Product</button>
    <button onclick="showProfile()">Profile</button>
    <button onclick="logout()">Logout</button>
  `:
  `
    <button onclick="showLogin()">Login</button>
    <button onclick="showRegister()">Register</button>
  `;
}

function showLogin(){
  app.innerHTML=`
    <div class="container">
      <h2>Login</h2>
      <input id="email" placeholder="Email">
      <input id="password" type="password" placeholder="Password">
      <button class="action" onclick="login()">Login</button>
    </div>
  `;
}

function showRegister(){
  app.innerHTML=`
    <div class="container">
      <h2>Register</h2>
      <input id="email">
      <input id="password" type="password">
      <button class="action" onclick="register()">Register</button>
    </div>
  `;
}

async function login(){

  const res = await fetch(API.auth+"/login",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      email: email.value,
      password: password.value
    })
  });

  const data = await res.json();

  if(!res.ok){
    alert(data.detail || "Login failed");
    return;
  }

  state.user = data;
  renderNav();
  loadProducts();
}

async function register(){
  await fetch(API.auth+"/register",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({email:email.value,password:password.value})
  });
  alert("Registered");
  showLogin();
}

function logout(){
  state.user=null;
  state.cart=[];
  renderNav();
  showLogin();
}

async function loadProducts(){
  const res=await fetch(API.products);
  const products=await res.json();

  app.innerHTML=`
  <div class="container">
    <h2>Store</h2>
    <div class="grid">
      ${products.map(p=>`
        <div class="card">
          <img src="${p.image||'https://via.placeholder.com/200'}">
          <h3>${p.name}</h3>
          <p>$${p.price}</p>
          <button class="action" onclick="addToCart(${p.id})">Add</button>
          <button class="action" onclick="editProduct(${p.id})">Edit</button>
          <button class="action danger" onclick="deleteProduct(${p.id})">Delete</button>
        </div>
      `).join('')}
    </div>
  </div>
  `;
}

function showCreateProduct(){
  app.innerHTML=`
    <div class="container">
      <h2>Create Product</h2>
      <input id="name" placeholder="Name">
      <input id="price" placeholder="Price">
      <input id="image" placeholder="Image URL">
      <button class="action" onclick="createProduct()">Create</button>
    </div>
  `;
}

async function createProduct(){
  await fetch(API.products,{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      name:name.value,
      price:Number(price.value),
      image:image.value
    })
  });

  loadProducts();
}

async function editProduct(id){
  const res=await fetch(API.products);
  const products=await res.json();
  const p=products.find(x=>x.id===id);

  app.innerHTML=`
    <div class="container">
      <h2>Edit Product</h2>
      <input id="name" value="${p.name}">
      <input id="price" value="${p.price}">
      <input id="image" value="${p.image}">
      <button class="action" onclick="updateProduct(${id})">Save</button>
    </div>
  `;
}

async function updateProduct(id){
  await fetch(API.products+"/"+id,{method:"PUT",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      name:name.value,
      price:Number(price.value),
      image:image.value
    })
  });

  loadProducts();
}

async function deleteProduct(id){
  if(!confirm("Delete?"))return;

  await fetch(API.products+"/"+id,{method:"DELETE"});
  loadProducts();
}

function addToCart(id){
  if(!state.user)return showLogin();

  fetch(API.products)
    .then(r=>r.json())
    .then(data=>{
      const p=data.find(x=>x.id===id);
      state.cart.push(p);
      renderNav();
    });
}

function showCart(){
  app.innerHTML=`
  <div class="container">
    <h2>Cart</h2>
    ${state.cart.map((p,i)=>`
      <div class="card">
        ${p.name} - $${p.price}
        <button onclick="removeFromCart(${i})">Remove</button>
      </div>
    `).join('')}
    <button class="action" onclick="checkout()">Checkout</button>
  </div>
  `;
}

function removeFromCart(i){
  state.cart.splice(i,1);
  showCart();
  renderNav();
}

async function checkout(){
  await fetch(API.orders,{method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({items:state.cart})
  });

  state.cart=[];
  alert("Order placed");
  loadProducts();
}

function showProfile(){
  app.innerHTML=`
  <div class="container">
    <h2>Profile</h2>
    <input id="newEmail" value="${state.user.email}">
    <input id="newPassword" placeholder="New password">
    <button class="action" onclick="updateProfile()">Save</button>
    <button class="action danger" onclick="deleteAccount()">Delete</button>
  </div>
  `;
}

async function updateProfile() {
  const email = newEmail.value.trim();
  const password = newPassword.value.trim();

  const res = await fetch(`${API.user}/update/${state.user.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email,
      password: password || undefined 
    })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Не удалось обновить профиль");
    return;
  }

  state.user = data;
  alert("Профиль обновлен");
  renderNav();
}

async function deleteAccount() {
  if (!confirm("Вы уверены, что хотите удалить аккаунт?")) return;


  const res = await fetch(`${API.user}/delete/${state.user.id}`, {
    method: "DELETE"
  });

  if (res.ok) {
    alert("Аккаунт успешно удален");
    logout(); 
  } else {
    const data = await res.json();
    alert(data.detail || "Ошибка при удалении");
  }
}



renderNav();
showLogin();
