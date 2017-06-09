function Location(data) {
    this.address = data.address;
    this.latitude = Number(data.latitude);
    this.longitude = Number(data.longitude);
}

Location.prototype.render = function () {
    return (
        '<tr>' +
            '<td>' + this.address + '</td>' +
            '<td>' + this.latitude + '</td>' +
            '<td>' + this.longitude + '</td>' +
        '</tr>'
    )
};
