import functools
from flask import jsonify
import logging
import traceback

logger = logging.getLogger(__name__)

def handle_errors(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Log the full exception traceback
            logger.error(f"Error in {f.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Return a JSON error response
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500
    return wrapped

