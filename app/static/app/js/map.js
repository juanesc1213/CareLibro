
var Icono = L.icon({
    iconUrl: "https://cdn-icons-png.flaticon.com/512/3277/3277422.png",
    iconSize: [30, 30],
    iconAnchor: [15, 40],
    popupAnchor: [0, -40]});
  
  
  let myMap = L.map('myMap').setView([4.8148635,-75.6958533], 14)
  
  L.tileLayer(`https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png`, {
      maxZoom: 18,
  }).addTo(myMap);
  
  const imglibro = "https://pbs.twimg.com/profile_images/1005326626870132736/QnrvpLpw_400x400.jpg"
  
  const tienda = L.marker([4.814772,-75.695578],{
    title: "tienda primera",
    icon: Icono,
  }).addTo(myMap).bindPopup(`
  <h5>Tienda CareLibro</h5>
  <p>tienda que vende libros para su cara</p>
  <img src=${imglibro}>
  `);
  
  let iconMarker = L.icon({
      iconUrl: 'marker.png',
      iconSize: [60, 60],
      iconAnchor: [30, 60]
  })
  
  
  
  
  