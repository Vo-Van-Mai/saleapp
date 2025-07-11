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
        let items = document.getElementsByClassName("cart-quantity");
        for (let item of items)
            item.innerText = data.Total_quantity;
     })
}