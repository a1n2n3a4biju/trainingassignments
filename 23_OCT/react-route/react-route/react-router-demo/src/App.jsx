import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  useParams,
  useNavigate
} from "react-router-dom"
 
import { useEffect, useState } from "react"
 
const API_URL = "http://127.0.0.1:8000/products"
 
// Home Page
function Home() {
  const navigate = useNavigate()
 
  return (
<div>
<h1>Home</h1>
<p>Welcome to the Product Store</p>
 
      <button onClick={() => navigate("/products")}>
        View Products
</button>
</div>
  )
}
 
// Products Page - GET, PUT and DELETE
function Products() {
  const [products, setProducts] = useState([])
  const [error, setError] = useState("")
  const [editingId, setEditingId] = useState(null)
 
  const [name, setName] = useState("")
  const [price, setPrice] = useState("")
  const [image, setImage] = useState("")
 
  async function loadProducts() {
    try {
      const response = await fetch(API_URL)
 
      if (!response.ok) {
        throw new Error("Failed to load products")
      }
 
      const data = await response.json()
      setProducts(data)
      setError("")
    } catch (err) {
      setError("Could not load products. Check FastAPI.")
    }
  }
 
  useEffect(() => {
    loadProducts()
  }, [])
 
  // Start editing a product
  function startEdit(product) {
    setEditingId(product.id)
    setName(product.name)
    setPrice(String(product.price))
    setImage(product.image)
    setError("")
  }
 
  // PUT - Update product
  async function updateProduct(event) {
    event.preventDefault()
    setError("")
 
    const updatedProduct = {
      id: editingId,
      name,
      price: Number(price),
      image
    }
 
    try {
      const response = await fetch(
        `${API_URL}/${editingId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(updatedProduct)
        }
      )
 
      const data = await response.json()
 
      if (!response.ok) {
        throw new Error(data.detail || "Update failed")
      }
 
      setEditingId(null)
      await loadProducts()
      alert("Product updated successfully!")
    } catch (err) {
      setError(err.message)
    }
  }
 
  // DELETE - Remove product
  async function removeProduct(id) {
    if (!window.confirm("Are you sure you want to delete this product?")) {
      return
    }
 
    setError("")
 
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
      })
 
      const data = await response.json()
 
      if (!response.ok) {
        throw new Error(data.detail || "Delete failed")
      }
 
      setProducts((current) =>
        current.filter((product) => product.id !== id)
      )
 
      if (editingId === id) {
        setEditingId(null)
      }
 
      alert("Product deleted successfully!")
    } catch (err) {
      setError(err.message)
    }
  }
 
  return (
<div>
<h1>Product Store</h1>
 
      {error && <p style={{ color: "red" }}>{error}</p>}
 
      {products.map((product) => (
<div key={product.id}>
<img
            src={product.image}
            alt={product.name}
            width="180"
          />
 
          <h2>{product.name}</h2>
<p>Product ID: {product.id}</p>
<p>Price: ₹{product.price}</p>
 
          <Link to={`/products/${product.id}`}>
            View Details
</Link>
 
          {" "}
 
          <button onClick={() => startEdit(product)}>
            Edit
</button>
 
          {" "}
 
          <button onClick={() => removeProduct(product.id)}>
            Delete
</button>
 
          {editingId === product.id && (
<form onSubmit={updateProduct}>
<h3>Edit Product</h3>
 
              <input
                type="text"
                placeholder="Product Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
 
              <br /><br />
 
              <input
                type="number"
                placeholder="Price"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                min="0"
                step="0.01"
                required
              />
 
              <br /><br />
 
              <input
                type="url"
                placeholder="Image URL"
                value={image}
                onChange={(e) => setImage(e.target.value)}
                required
              />
 
              <br /><br />
 
              <button type="submit">
                Save Changes
</button>
 
              {" "}
 
              <button
                type="button"
                onClick={() => setEditingId(null)}
>
                Cancel
</button>
</form>
          )}
 
          <hr />
</div>
      ))}
</div>
  )
}
 
// Product Details Page - GET by ID
function ProductDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
 
  const [product, setProduct] = useState(null)
  const [error, setError] = useState("")
 
  useEffect(() => {
    async function fetchProduct() {
      try {
        const response = await fetch(`${API_URL}/${id}`)
 
        if (!response.ok) {
          throw new Error("Product not found")
        }
 
        const data = await response.json()
        setProduct(data)
      } catch (err) {
        setError(err.message)
      }
    }
 
    fetchProduct()
  }, [id])
 
  return (
<div>
<h1>Product Details</h1>
 
      {error && <p>{error}</p>}
 
      {product && (
<div>
<img
            src={product.image}
            alt={product.name}
            width="200"
          />
 
          <h2>{product.name}</h2>
<p>Product ID: {product.id}</p>
<p>Price: ₹{product.price}</p>
</div>
      )}
 
      <button onClick={() => navigate("/products")}>
        Back to Products
</button>
</div>
  )
}
 
// Add Product Page - POST
function AddProduct() {
  const navigate = useNavigate()
 
  const [id, setId] = useState("")
  const [name, setName] = useState("")
  const [price, setPrice] = useState("")
  const [image, setImage] = useState("")
  const [message, setMessage] = useState("")
 
  async function saveProduct(event) {
    event.preventDefault()
    setMessage("")
 
    const product = {
      id: Number(id),
      name,
      price: Number(price),
      image
    }
 
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(product)
      })
 
      const data = await response.json()
 
      if (!response.ok) {
        throw new Error(data.detail || "Failed to add product")
      }
 
      alert("Product added successfully!")
      navigate("/products")
    } catch (err) {
      setMessage(err.message)
    }
  }
 
  return (
<div>
<h1>Add Product</h1>
 
      <form onSubmit={saveProduct}>
<input
          type="number"
          placeholder="Product ID"
          value={id}
          onChange={(e) => setId(e.target.value)}
          required
          min="1"
        />
 
        <br /><br />
 
        <input
          type="text"
          placeholder="Product Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
 
        <br /><br />
 
        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
          min="0"
          step="0.01"
        />
 
        <br /><br />
 
        <input
          type="url"
          placeholder="Image URL"
          value={image}
          onChange={(e) => setImage(e.target.value)}
          required
        />
 
        <br /><br />
 
        <button type="submit">
          Save Product
</button>
</form>
 
      {message && (
<p style={{ color: "red" }}>{message}</p>
      )}
</div>
  )
}
 
// About Page
function About() {
  return (
<div>
<h1>About</h1>
<p>Simple React Product Store connected to FastAPI.</p>
</div>
  )
}
 
// Main App
function App() {
  return (
<BrowserRouter>
<nav>
<Link to="/">Home</Link>
        {" | "}
<Link to="/products">Products</Link>
        {" | "}
<Link to="/about">About</Link>
        {" | "}
<Link to="/addproducts">Add Products</Link>
</nav>
 
      <hr />
 
      <Routes>
<Route path="/" element={<Home />} />
<Route path="/products" element={<Products />} />
<Route path="/products/:id" element={<ProductDetails />} />
<Route path="/about" element={<About />} />
<Route path="/addproducts" element={<AddProduct />} />
</Routes>
</BrowserRouter>
  )
}
 
export default App