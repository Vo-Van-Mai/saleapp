function Update(data){
    let items = document.getElementsByClassName("cart-quantity");
    for (let item of items)
        item.innerText = data.Total_quantity;

    let amount = document.getElementsByClassName("cart-amount");
    for (let item of amount)
        item.innerText = data.Total_price.toLocaleString();
}


function AddToCart(id, name, price){
    fetch("/api/cart",{
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers:{
            'Content-Type': 'application/json'
         }
     }).then(res => res.json()).then(data => {
        console.info(data);
        Update(data);
        })
}


function UpdateCart(productId, obj) {
    fetch(`/api/carts/${productId}`, {
        method: "PUT",
        body: JSON.stringify({
        quantity: obj.value
        }),
        headers:{
            "Content-Type": 'application/json'
        }
    }).then(res => res.json()).then(data => {
        Update(data);
    })
}

function deleteCart(productId) {
    if (confirm("Bạn có chắc chắn muốn xóa sản phẩm không?") == true){
        fetch(`/api/carts/${productId}`, {
        method: "delete"
        }).then(res => res.json()).then(data => {
            Update(data);
            document.getElementById(`cart${productId}`).style.display= "none"
        })
    }
}

function pay() {
    if (confirm("Bạn có chắc chắn muốn thanh toán không?") == true){
        fetch("/api/pay", {
            method: "post"
        }).then(res => res.json()).then(data => {
            if(data.status===200)
                alert("Thanh toán thành công!");
                location.reload();
        })
    }
}
