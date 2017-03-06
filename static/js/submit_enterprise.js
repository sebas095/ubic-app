/**
 * Created by sebastian on 3/03/17.
 */

const form = document.getElementById('form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    const {p1, p2, p3, p4} = this;
    const nit = `${p1.value}.${p2.value}.${p3.value}-${p4.value}`;
    document.getElementById("id_nit").value = nit;
    this.submit();
});