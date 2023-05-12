import React from 'react'
import {WEAPON_SLOTS, ARMOR_SLOTS} from '../../../const/Items.js'
import { BUNGIE_URL } from '../../../const/BungieUrl.js';
const GuardianEquipment = ({guardian}) => {
    let items = Object.entries(guardian.items);
    const weapons = items.filter((item) => WEAPON_SLOTS.includes(item[0]));
    const armor = items.filter((item) => ARMOR_SLOTS.includes(item[0]));

  return (
		<div className='flex flex-row justify-around m-5'>
			<div className='flex flex-col'>
				{weapons.map((weapon) => (
					<div
						key={weapon[0]}
						className='m-3 cursor-pointer'>
                            <div className="relative">
						<img
							src={BUNGIE_URL + weapon[1].common_data.item_icon}
							alt='Zen'
							width={95}
							height={95}
							className='mx-auto my-auto rounded-lg'></img>
						<img
							src={BUNGIE_URL + weapon[1].common_data.item_watermark}
							alt='Zen'
							width={95}
							className='absolute top-0 start-0'
							height={95}></img>
                            </div>
					</div>
				))}
			</div>
			<div className='flex flex-col'>
				{armor.map((armor) => (
					<div
						key={armor[0]}
						className='m-3 cursor-pointer'>
                            <div className="relative">
						<img
							src={BUNGIE_URL + armor[1].common_data.item_icon}
							alt='Zen'
							width={95}
							height={95}
							className='mx-auto my-auto rounded-lg'></img>
                            <img
                            src={BUNGIE_URL + armor[1].common_data.item_watermark}
                            alt='Zen'
                            width={95}
                            className='absolute top-0 start-0'
                            height={95}></img>
                            </div>
					</div>
				))}
			</div>
		</div>
	);
}

export default GuardianEquipment