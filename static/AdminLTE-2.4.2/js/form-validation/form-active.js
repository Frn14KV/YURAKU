(function ($) {
 "use strict";
 // Validacion del Tutor
		$(".add-professors").validate(
		{					
			rules:
			{	
				nombre_tutor:
				{
					required: true
				},
				apellido_tutor:
				{
					required: true
				},
				cedula_tutor:
				{
					required: true
				},
				correo_tutor:
				{
					required: true
				},
				telefono_tutor:
				{
					required: true
				},
				imagen_tutor:
				{
					required: false
				},
				Carrera_tutor:
				{
					required: true
				}
			},
			messages:
			{	
				nombre_tutor:
				{
					required: 'Por favor ingrese el nombre del Tutor.'
				},
				apellido_tutor:
				{
					required: 'Por favor ingrese el apellido del Tutor.'
				},
				cedula_tutor:
				{
					required: 'Por favor ingrese el número de cédula del Tutor.'
				},
				correo_tutor:
				{
					required: 'Por favor ingrese el correo electrónico del Tutor.'
				},
				telefono_tutor:
				{
					required: 'Por favor ingrese el número de teléfono del Tutor.'
				},
				imagen_tutor:
				{
					required: 'Por favor ingrese una imagen para el Tutor.'
				},
				Carrera_tutor:
				{
					required: 'Por favor seleccione la Carrera para el Tutor.'
				}
			},					
			
			errorPlacement: function(error, element)
			{
				error.insertAfter(element.parent());
			}
		});



     // Validacion del Autor
		$(".addcoursepro").validate(
		{
			rules:
			{
				nombre_autor:
				{
					required: true
				},
				apellido_autor:
				{
					required: true
				},
				cedula_autor:
				{
					required: true
				},
				correo_autor:
				{
					required: true,
					email: true
				},
				telefono_autor:
				{
					required: true
				},
				imagen_autor:
				{
					required: false
				},
				Carrera_autor:
				{
					required: true
				}
			},
			messages:
			{
				nombre_autor:
				{
					required: 'Por favor ingrese el nombre del Autor.'
				},
				apellido_autor:
				{
					required: 'Por favor ingrese el apellido del Autor.'
				},
				cedula_autor:
				{
					required: 'Por favor ingrese el número de cédula del Autor.'
				},
				correo_autor:
				{
					required: 'Por favor ingrese el correo electrónico del Autor.',
					correo: 'Por favor ingrese un correo VALIDO.'
				},
				telefono_autor:
				{
					required: 'Por favor ingrese el número de teléfono del Autor.'
				},
				imagen_autor:
				{
					required: 'Por favor ingrese una imagen para el Autor.'
				},
				Carrera_autor:
				{
					required: 'Por favor seleccione la Carrera para el Autor.'
				}
			},

			errorPlacement: function(error, element)
			{
				error.insertAfter(element.parent());
			}
		});


		// Validacion del Responsable
		$(".add-department").validate(
		{
			rules:
			{
				nombre_responsable:
				{
					required: true
				},
				apellido_responsable:
				{
					required: true
				},
				cedula_responsable:
				{
					required: true
				},
				correo_responsable:
				{
					required: true
				},
				telefono_responsable:
				{
					required: true
				},
				imagen_responsable:
				{
					required: false
				},
				Institucion:
				{
					required: true
				}
			},
			messages:
			{
				nombre_responsable:
				{
					required: 'Por favor ingrese el nombre del Responsable.'
				},
				apellido_responsable:
				{
					required: 'Por favor ingrese el apellido del Responsable.'
				},
				cedula_responsable:
				{
					required: 'Por favor ingrese el número de cédula del Responsable.'
				},
				correo_responsable:
				{
					required: 'Por favor ingrese el correo electrónico del Responsable.'
				},
				telefono_responsable:
				{
					required: 'Por favor ingrese el número de teléfono del Responsable.'
				},
				imagen_responsable:
				{
					required: 'Por favor ingrese una imagen para el Responsable.'
				},
				Institucion:
				{
					required: 'Por favor seleccione la Institución para el Responsable.'
				}
			},

			errorPlacement: function(error, element)
			{
				error.insertAfter(element.parent());
			}
		});
		

 // Validacion de la Institucion
		$(".addcourse").validate(
		{					
			rules:
			{	
				nombre_institucion:
				{
					required: true
				},
				direccion_institucion:
				{
					required: true
				},
				telefono_institucion:
				{
					required: true
				},
				imagen_institucion:
				{
					required: false
				},
				descripcion_institucion:
				{
					required: true
				},
				correo_institucion:
				{
					required: true,
					email: true
				}
			},
			messages:
			{	
				nombre_institucion:
				{
					required: 'Por favor ingrese el nombre de la Institución.'
				},
				direccion_institucion:
				{
					required: 'Por favor ingrese la dirección de la Institución.'
				},
				telefono_institucion:
				{
					required: 'Por favor ingrese el número de la Institución.'
				},
				imagen_institucion:
				{
					required: 'Por favor ingrese una imagen de la Institución.'
				},
				descripcion_institucion:
				{
					required: 'Por favor ingrese una breve descripción de la Institución.'
				},
				correo_institucion:
				{
					required: 'Por favor ingrese el correo de la Institución.',
					correo: 'Por favor ingrese un correo VALIDO.'
				}
			},					
			
			errorPlacement: function(error, element)
			{
				error.insertAfter(element.parent());
			}
		});
		

 
	// Validacion de la Carrera
		$(".carrera").validate(
		{					
			rules:
			{	
				nombre_carrera:
				{
					required: true
				},
				descripcion_carrera:
				{
					required: true
				}
			},
			messages:
			{	
				nombre_carrera:
				{
					required: 'Por favor ingrese el nombre de la Carrera.'
				},
				descripcion_carrera:
				{
					required: 'Por favor ingrese una descripción de la Carrera.'
				}
			},					
			
			errorPlacement: function(error, element)
			{
				error.insertAfter(element.parent());
			}
		});



    // Validacion de la Area de Conocimiento
		$(".area").validate(
		{
			rules:
			{
				nombre_area:
				{
					required: true
				},
				descripcion_area:
				{
					required: true
				}
			},
			messages:
			{
				nombre_area:
				{
					required: 'Por favor ingrese el nombre del Área de Conocimiento.'
				},
				descripcion_area:
				{
					required: 'Por favor ingrese una descripción del Área de Conocimiento.'
				}
			},

			errorPlacement: function(error, element)
			{
				error.insertAfter(element.parent());
			}
		});



       // Validacion de la Tipo de Proyecto
		$(".tipo").validate(
		{
			rules:
			{
				nombre_tipo:
				{
					required: true
				},
				descripcion_tipo:
				{
					required: true
				}
			},
			messages:
			{
				nombre_tipo:
				{
					required: 'Por favor ingrese el nombre del Tipo de Proyecto.'
				},
				descripcion_tipo:
				{
					required: 'Por favor ingrese una descripción del Tipo de Proyecto.'
				}
			},

			errorPlacement: function(error, element)
			{
				error.insertAfter(element.parent());
			}
		});



	// Validacion del Proyecto
		$(".comment").validate(
		{					
			rules:
			{	
				Titulo:
				{
					required: true
				},
				Institucion:
				{
					required: true
				},
				TipoProyecto:
				{
					required: true
				},
				Proposito:
				{
					required: true
				},
				Tutor:
				{
					required: true
				},
				Autor:
				{
					required: true
				},
				AreaConocimiento:
				{
					required: true
				},
				ResponsableInstitucional:
				{
					required: true
				},
				Estado_proyecto:
				{
					required: true
				},
				Poblacion_utiliza:
				{
					required: true
				},
				Numero_muestra_ninos:
				{
					required: true
				},
				Donado:
				{
					required: true
				},
				Fecha_Donacion:
				{
					required: true
				},
				Tiempo_inactividad:
				{
					required: true
				},
				Sugerencias:
				{
					required: true
				}
			},
			messages:
			{	
				Titulo:
				{
					required: 'Por favor ingrese el Titulo del Proyecto.'
				},
				Institucion:
				{
					required: 'Por favor selecione la o las Insituciones para el Proyecto.'
				},
				TipoProyecto:
				{
					required: 'Por favor selecione el o los Tipos de Poryecto.'
				},
				ResponsableInstitucional:
				{
					required: 'Por favor selecione el o los Responsables del Proyecto.'
				},
				Proposito:
				{
					required: 'Por favor escriba el Proposito del Proyecto.'
				},
				Tutor:
				{
					required: 'Por favor selecione el o los Tutores del Proyecto.'
				},
				Autor:
				{
					required: 'Por favor selecione el o los Autores del Proyecto.'
				},
				AreaConocimiento:
				{
					required: 'Por favor selecione el o las Áreas de Conocimiento del Proyecto.'
				},
				Estado_proyecto:
				{
					required: 'Por favor escriba el estado del Proyecto.'
				},
				Poblacion_utiliza:
				{
					required: 'Por favor escriba la Poblacion que utiliza el Proyecto.'
				},
				Numero_muestra_ninos:
				{
					required: 'Por favor escriba el Numero de Muestras de Niños'
				},
				Donado:
				{
					required: 'Por favor seleciones si el Poryecto es donado.'
				},
				Fecha_Donacion:
				{
					required: 'Por favor selecione la fecha de donacion del Proyecto.'
				},
				Tiempo_inactividad:
				{
					required: 'Por favor escriba el tiempo de inactividad del Proyecto.'
				},
				Sugerencias:
				{
					required: 'Por favor escriba alguna sugerencia del Proyecto.'
				}
			},					
			
			errorPlacement: function(error, element)
			{
				error.insertAfter(element.parent());
			}
		});

		// Validacion del Usuario
		$(".add-user").validate(
		{
			rules:
			{
				first_name:
				{
					required: true
				},
				last_name:
				{
					required: true
				},
				username:
				{
					required: true
				},
				email:
				{
					required: true
				},
				email1:
				{
					required: true
				},
				password2:
				{
					required: true
				},
                password1:
				{
					required: true
				},
				typeuser:
				{
					required: true
				}
			},
			messages:
			{
				first_name:
				{
					required: 'Por favor ingrese el nombre del Usuario.'
				},
				last_name:
				{
					required: 'Por favor ingrese el apellido del Usuario.'
				},
				username:
				{
					required: 'Por favor ingrese el username para el Usuario.'
				},
				email:
				{
					required: 'Por favor ingrese el correo electrónico para el Usuario.',
					email: 'Por favor ingrese un correo VALIDO.'
				},
				email1:
				{
					required: 'Por favor ingrese el correo electrónico para el Usuario.'
				},
				password2:
				{
					required: 'Por favor ingrese una clave para el Usuario.'
				},
                password1:
				{
					required: 'Por favor ingrese una clave para el Usuario.'
				},
				typeuser:
				{
					required: 'Por favor seleccione el tipo de rol para el Usuario.'
				}
			},

			errorPlacement: function(error, element)
			{
				error.insertAfter(element.parent());
			}
		});

})(jQuery); 