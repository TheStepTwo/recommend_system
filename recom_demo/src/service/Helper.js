import Vue from 'vue'
export const Helper = {
	data() {
		return {}
	},
	methods: {
		_checkDate(payDate) {
			if (payDate == "") return true;
			var formatedDateString = Date.parse(payDate.substring(0, 4) + "-" + payDate.substring(4, 6) + "-" + payDate.substring(6, 8));
			if (payDate.length != 8 || formatedDateString < 0) {
				return false;
			}
			return true;
		},
		_trueFalseTrans(value, trueDisplay, falseDisplay) {
			if ( value == undefined || value == null ){
				return value;
			}else if ( value.trim() == "" ){
				return value;
			}
			return value? trueDisplay: falseDisplay;
		},
	}
};
