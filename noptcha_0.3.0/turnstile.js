(async()=>{for(;;){await Time.sleep(1e3);var e=await BG.exec("get_settings");e&&e.enabled&&e.turnstile_auto_solve&&document.querySelector("#not_a_bot")?.click()}})();
