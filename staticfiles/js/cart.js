function addToCart(event, productId) {
    event.preventDefault(); // предотвращаем стандартное поведение формы (перезагрузку)
  
    fetch(`/add-to-cart/${productId}/`, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        // заменяем форму на блок с + / - и количеством
        const container = document.getElementById(`product-${productId}`);
        container.innerHTML = `
          <div>
            <button onclick="updateCart(${productId}, 'decrement')">-</button>
            <span id="qty-${productId}">${data.quantity}</span>
            <button onclick="updateCart(${productId}, 'increment')">+</button>
          </div>
        `;
      }
    });
  }
  
  function updateCart(productId, action) {
    fetch(`/update-cart/${productId}/${action}/`, {
      headers: {'X-Requested-With': 'XMLHttpRequest'}
    })
    .then(res => res.json())
    .then(data => {
      if (data.quantity > 0) {
        document.getElementById(`qty-${productId}`).innerText = data.quantity;
      } else {
        location.reload();
      }
    });
  }
  