const select = document.getElementById("backupSelect");
const savename = document.getElementById("saveworldname");
const savedesc = document.getElementById("saveworlddesc");
const editname = document.getElementById("editworldname");
const editdesc = document.getElementById("editworlddesc");

const getSelectedId = () => {
    return Number(select.value);
}

const updateSelect = (backups) => {
    select.innerHTML = "";
    for (let b of backups) {
        const option = document.createElement("option");
        option.value = b.id;
        option.innerHTML = b.name
        select.appendChild(option)
    }
    onBackupSelect();
}

const resetModifyInfo = () => {
    editname.value = ""
    editdesc.value = ""
}

const updateModifyInfo = (name, desc) => {
    editname.value = name
    editdesc.value = desc
}

const onBackupSelect = () => {
    const id = getSelectedId()
    GetBackups().then(backups => {
        resetModifyInfo();

        for (let b of backups) {
            if (b.id == id) {
                updateModifyInfo(b.name, b.description)
                break;
            }
        }
    })
}

const onSaveWorld = () => {
    SaveWorld(savename.value, savedesc.value).then(r => {
        updateSelect(r);
    })
}

const onLoadWorld = () => {
    const id = getSelectedId();
    if (id !== null && id !== undefined) {
        LoadWorld(id);
    }
}

const onRemoveBackup = () => {
    const id = getSelectedId();
    RemoveBackup(id).then(backups => {
        updateSelect(backups);
    })
}

const onModifyBackup = () => {
    const id = getSelectedId();
    let name = editname.value
    let desc = editdesc.value;

    ModifyBackup(id, name, desc).then(r => {
        updateSelect(r)
    })
}

GetBackups().then(r => {
    updateSelect(r)
    if (r.length > 0) {
        updateModifyInfo(r[0].name, r[0].description)
    }
})