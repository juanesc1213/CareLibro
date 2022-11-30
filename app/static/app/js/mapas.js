// Icono variable con la imagen,tamaño, etc

var Icono = L.icon({
    iconUrl: "https://cdn-icons-png.flaticon.com/512/3277/3277422.png",
    iconSize: [30, 30],
    iconAnchor: [15, 40],
    popupAnchor: [0, -40]});
  
  //el mapa principal y en donde coordenadas arranca
  let myMap = L.map('myMap').setView([4.8148635,-75.6958533], 14)
  
  //como carga el mapa que tipo de mapa va usar para mostrar
  L.tileLayer(`https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png`, {
      maxZoom: 18,
  }).addTo(myMap);
  
  //imagen al darle click a un marcador del mapa
  

   
  //marcador
  const tienda = L.marker([4.8150615,-75.7054435],{
    title: "tienda primera",
    icon: Icono,
  }).addTo(myMap).bindPopup(`
  <h5>Tienda CareLibro</h5>
  <p>Tienda del Centro</p>
  `);

  const tienda2 = L.marker([4.811374, -75.703993],{
    title: "tienda primera",
    icon: Icono,
  }).addTo(myMap).bindPopup(`
  <h5>Tienda CareLibro</h5>
  <p>Tienda sede 30 de Agosto</p>
  `);

 /*  datos = [
    { 'latitud': 4.8140615, 'longitud': -75.674435 },

];

for (var i=0; datos.length; i++) {
    L.marker([datos[i].latitud, datos[i].longitud],{
      title: "tienda primera",
      icon: Icono,
    }).addTo(myMap);        
}; */
  



  
  
  