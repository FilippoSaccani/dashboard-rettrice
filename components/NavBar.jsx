function NavItem(props) {
    return (
        <a class={"navbar-item navbar-choice " + (props.selected ? "selected" : "unselected")} href="#">
            {props.icon}
            <h2>{props.title}</h2>
        </a>
    );
}

function NavBar(props) {
    let title = "";
    switch (props.selected){
        case 0: title = "Social Media";
            break;
        case 1: title = "Rassegna stampa";
            break;
        case 2: title = "Amministrazione";
            break;
        default: throw new Error("Prop non valide");
    }

    let selected = [false, false, false];
    selected[props.selected] = true;

    return (
        <div class="navbar">
            <div class="left">
                <div class="background-red navbar-item"><i class="fa-solid fa-chart-column color-white"></i></div>
                <h1>{title}</h1>
            </div>

            <div class="right">
                <NavItem title="Social Media" selected={selected[0]} icon={<i class="fa-solid fa-chart-column"></i>}/>
                <NavItem title="Rassegna stampa" selected={selected[1]} icon={<i class="fa-regular fa-file-lines"></i>}/>
                <NavItem title="Amministrazione" selected={selected[2]} icon={<i class="fa-solid fa-plus"></i>}/>
            </div>
        </div>
    )
}

export default NavBar;