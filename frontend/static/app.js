const userForm = document.getElementById("userForm");
const userIdInput = document.getElementById("userId");
const nombreInput = document.getElementById("nombre");
const emailInput = document.getElementById("email");
const formTitle = document.getElementById("formTitle");
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");
const usersTableBody = document.getElementById("usersTableBody");
const alertBox = document.getElementById("alertBox");

// Mostrar notificaciones
function showAlert(message, type = "success") {
    alertBox.textContent = message;
    alertBox.className = `alert ${type}`;
    setTimeout(() => alertBox.classList.add("hidden"), 3500);
}

// 1. READ (GET /users)
async function cargarUsuarios() {
    try {
        const res = await fetch(`${API_URL}/users`);
        const usuarios = await res.json();
        usersTableBody.innerHTML = "";

        usuarios.forEach(user => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${user.id}</td>
                <td>${user.nombre}</td>
                <td>${user.email}</td>
                <td>
                    <button class="btn-edit" onclick="prepararEdicion(${user.id}, '${user.nombre}', '${user.email}')">Editar</button>
                    <button class="btn-delete" onclick="eliminarUsuario(${user.id})">Eliminar</button>
                </td>
            `;
            usersTableBody.appendChild(tr);
        });
    } catch (error) {
        showAlert("Error al conectar con el backend", "error");
    }
}

// 2. CREATE (POST) y UPDATE (PUT)
userForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = userIdInput.value;
    const payload = {
        nombre: nombreInput.value.trim(),
        email: emailInput.value.trim()
    };

    try {
        let res;
        if (id) {
            // Modo Edición -> PUT
            res = await fetch(`${API_URL}/users/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
        } else {
            // Modo Creación -> POST
            res = await fetch(`${API_URL}/users`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
        }

        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.detail || "Error en la operación");
        }

        showAlert(id ? "Usuario actualizado correctamente" : "Usuario creado correctamente");
        resetearFormulario();
        cargarUsuarios();
    } catch (error) {
        showAlert(error.message, "error");
    }
});

// Preparar el formulario para editar
function prepararEdicion(id, nombre, email) {
    userIdInput.value = id;
    nombreInput.value = nombre;
    emailInput.value = email;
    formTitle.textContent = `Editando Usuario #${id}`;
    submitBtn.textContent = "Guardar Cambios";
    cancelBtn.classList.remove("hidden");
}

function resetearFormulario() {
    userForm.reset();
    userIdInput.value = "";
    formTitle.textContent = "Nuevo Usuario";
    submitBtn.textContent = "Guardar Usuario";
    cancelBtn.classList.add("hidden");
}

cancelBtn.addEventListener("click", resetearFormulario);

// 3. DELETE (DELETE /users/{id})
async function eliminarUsuario(id) {
    if (!confirm(`¿Seguro que deseas eliminar al usuario #${id}?`)) return;

    try {
        const res = await fetch(`${API_URL}/users/${id}`, { method: "DELETE" });
        if (!res.ok) throw new Error("No se pudo eliminar el usuario");

        showAlert("Usuario eliminado");
        cargarUsuarios();
    } catch (error) {
        showAlert(error.message, "error");
    }
}

// Cargar la tabla al abrir la página
document.addEventListener("DOMContentLoaded", cargarUsuarios);
