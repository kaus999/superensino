let opcoes = ["id_exercicioalternativa_set-0-eal_eh_correta", "id_exercicioalternativa_set-1-eal_eh_correta", "id_exercicioalternativa_set-2-eal_eh_correta", "id_exercicioalternativa_set-3-eal_eh_correta"];

$(document).ready(function () {

    let marcada = false;

    setTimeout(() => {
        for (let outra of opcoes) {
            if ($('#' + outra).prop('checked')) {
                marcada = true;
            }
        }
        if (!marcada) {
            console.log('vixe')
            $('#' + opcoes[0]).prop('checked', true);
        }
    }, 500);

    for (let opcao of opcoes) {
        $('#' + opcao).change(function () {
            if (this.checked) {
                $(this).prop("checked", true);
                for (let outra of opcoes) {
                    if (outra !== opcao) {
                        $('#' + outra).prop("checked", false);
                    }
                }
            } else {
                setTimeout(() => {
                    marcada = false;
                    for (let outra of opcoes) {
                        if ($('#' + outra).checked) {
                            marcada = true;
                        }
                    }
                    if (!marcada) {
                        $(this).prop('checked', true);
                    }
                }, 500);

            }
        });
    }
});