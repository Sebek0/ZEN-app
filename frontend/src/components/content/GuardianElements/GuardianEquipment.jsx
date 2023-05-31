import React from "react";
import { ARMOR_SLOTS, WEAPON_SLOTS } from "../../../const/Items.js";
import Item from "./ItemElements/Item.jsx";
const GuardianEquipment = ({ guardian }) => {
	let items = Object.entries(guardian.items);
	const weapons = items.filter((item) => WEAPON_SLOTS.includes(item[0]));
	const armor = items.filter((item) => ARMOR_SLOTS.includes(item[0]));
	return (
		<div className='flex flex-col justify-center space-y-10'>
			<div className='flex flex-col'>
				{weapons.map((weapon) => (
					<Item
						key={weapon[0]}
						item={weapon}></Item>
				))}
			</div>
			<div className='flex flex-col'>
				{armor.map((armor) => (
					<Item
						key={armor[0]}
						item={armor}></Item>
				))}
			</div>
		</div>
	);
};

export default GuardianEquipment;
